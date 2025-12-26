create table if not exists franquicias (
    id uuid primary key default gen_random_uuid() not null,
    cuit varchar(11) not null unique,
    razon_social varchar(150) not null
);

create table if not exists usuarios (
    id uuid primary key default gen_random_uuid() not null,
    usuario varchar(30) not null unique,
    contra varchar(250) not null,
    activo bool not null default true,
    rol varchar(30) not null default 'OPERADOR',
    constraint ch_usu_rol check ( rol in ('SUPERADMIN', 'GESTOR', 'OPERADOR') )
);

create table if not exists operadores (
    id uuid primary key default gen_random_uuid() not null,
    id_usuario uuid not null,
    id_franquicia uuid not null,
    activo bool not null default true,
    constraint fk_ope_usu foreign key (id_usuario) references usuarios(id),
    constraint fk_ope_fra foreign key (id_franquicia) references franquicias(id),
    constraint un_ope unique(id_usuario, id_franquicia)
);

create table if not exists cargas (
    id uuid primary key default gen_random_uuid() not null,
    id_operador uuid not null,
    fecha_carga timestamp with time zone not null default now(),
    nombre_archivo varchar(150) not null unique,
    periodo date not null,
    status varchar(30) not null,
    constraint fk_car_ope foreign key (id_operador) references operadores(id),
    constraint check_car_sta check ( status in
                                     (
                                      'RAW',
                                      'VALIDATED',
                                      'TRANSFORMED',
                                      'LOADED',
                                      'VALIDATION FAILED',
                                      'TRANSFORM FAILED',
                                      'LOAD FAILED') )
);

create index if not exists idx_car_ope on cargas(id_operador);

create index if not exists  idx_car_sta on cargas(status);

create table if not exists audit_logs (
    id uuid primary key not null default gen_random_uuid(),
    id_operador uuid,
    tabla_afectada varchar(100),
    id_registro_afectado uuid not null,
    fecha_movimiento timestamp with time zone not null default now(),
    accion varchar(30) not null,
    valor_anterior jsonb,
    valor_actualizado jsonb,
    comentario varchar(300),
    constraint fk_aud_ope foreign key (id_operador) references operadores(id),
    constraint ch_aud_acc check ( accion in ('INSERT', 'UPDATE', 'DELETE', 'UPSERT') ),
    constraint ch_aud_tab check ( tabla_afectada in (
                                                     'franquicias',
                                                     'usuarios',
                                                     'operadores',
                                                     'cargas',
                                                     'audit_logs') )
);

create table if not exists health (
    id uuid primary key default gen_random_uuid() not null,
    status varchar(2) default 'OK' not null,
    fecha timestamp with time zone default now()
);

create table if not exists puntos_venta (
    id uuid primary key default gen_random_uuid() not null,
    descripcion varchar(100) not null,
    id_franquicia uuid not null,
    constraint fk_pv_fra foreign key (id_franquicia) references franquicias(id),
    constraint un_pv unique (descripcion, id_franquicia)
);

CREATE OR REPLACE FUNCTION obtener_franq_por_usuario(p_id_usuario uuid)
RETURNS TABLE (
    id uuid,
    cuit varchar(11),
    razon_social varchar(150) -- Coincide con la tabla
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT f.id, f.cuit, f.razon_social
    FROM franquicias f
    INNER JOIN operadores ope ON f.id = ope.id_franquicia
    WHERE ope.id_usuario = p_id_usuario; -- Usamos el parámetro
END;
$$;

alter table cargas add column id_punto_venta uuid not null;

alter table cargas add constraint fk_car_pv foreign key (id_punto_venta) references puntos_venta(id)

create function cargas_por_franquicia(p_id_franquicia uuid, p_id_usuario uuid)
    returns TABLE(id uuid, id_operador uuid, fecha_carga timestamp with time zone, nombre_archivo character varying, periodo date, status character varying, id_punto_venta uuid, ult_fecha_status timestamp with time zone)
    language plpgsql
as
$$
    begin
        return query
        select c.* from cargas as c
        inner join puntos_venta as pv
        on c.id_punto_venta = pv.id
        inner join franquicias
        on franquicias.id = pv.id_franquicia
        inner join operadores
        on c.id_operador = operadores.id
        inner join usuarios
        on operadores.id_usuario = usuarios.id
        where franquicias.id = p_id_franquicia and usuarios.id = p_id_usuario;
    end;
    $$;

alter table puntos_venta add column script varchar(150) default null