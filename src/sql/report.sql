-- Usuarios, asesores y subsistemas

select `a`.`username`, `a`.`email`, `b`.`nombre`, `b`.`nombre`, `b`.`appat`, `b`.`apmat`, `b`.`subsistema`, `asesor`.`nombre` `nombre_asesor`, `usuario_asesor`.`email` `correo_asesor` from `auth_user` `a`
left join `usuarios_perfil` `b` on `a`.`id` = `b`.`usuario_id`
left join `usuarios_perfil` `asesor` on `b`.`asesor_id` = `asesor`.id
left join `auth_user` `usuario_asesor` on `asesor`.`usuario_id` = `usuario_asesor`.`id`
where year(`a`.`date_joined`)=2014 and month(`a`.`date_joined`)=3