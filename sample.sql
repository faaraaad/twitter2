2023-09-06 09:53:55.868 UTC [77] LOG:  statement: SELECT set_config('TimeZone', 'UTC', false)
2023-09-06 09:53:55.869 UTC [77] LOG:  duration: 0.750 ms
2023-09-06 09:53:55.869 UTC [77] LOG:  statement: SELECT "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."date_joined" FROM "auth_user" WHERE "auth_user"."id" = 10732 LIMIT 21
2023-09-06 09:53:55.871 UTC [77] LOG:  duration: 1.804 ms
2023-09-06 09:53:55.872 UTC [77] LOG:  statement: SELECT "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."date_joined", "app_myuser"."user_ptr_id" FROM "app_myuser" INNER JOIN "auth_user" ON ("app_myuser"."user_ptr_id" = "auth_user"."id") WHERE "app_myuser"."user_ptr_id" = 10732 LIMIT 21
2023-09-06 09:53:55.873 UTC [77] LOG:  duration: 0.739 ms
2023-09-06 09:53:55.875 UTC [77] LOG:  statement: SELECT COUNT(*) AS "__count" FROM "app_post" WHERE "app_post"."author_id" IN (SELECT U0."user_ptr_id" FROM "app_myuser" U0 INNER JOIN "app_myuser_followings" U1 ON (U0."user_ptr_id" = U1."to_myuser_id") WHERE U1."from_myuser_id" = 10732)
2023-09-06 09:53:55.877 UTC [77] LOG:  duration: 1.981 ms
2023-09-06 09:53:55.878 UTC [77] LOG:  statement: SELECT "app_post"."id", "app_post"."author_id", "app_post"."body", "app_post"."create_at" FROM "app_post" WHERE "app_post"."author_id" IN (SELECT U0."user_ptr_id" FROM "app_myuser" U0 INNER JOIN "app_myuser_followings" U1 ON (U0."user_ptr_id" = U1."to_myuser_id") WHERE U1."from_myuser_id" = 10732) ORDER BY "app_post"."create_at" DESC LIMIT 5
2023-09-06 09:53:55.881 UTC [77] LOG:  duration: 2.075 ms
2023-09-06 09:53:55.882 UTC [77] LOG:  statement: SELECT "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."date_joined", "app_myuser"."user_ptr_id" FROM "app_myuser" INNER JOIN "auth_user" ON ("app_myuser"."user_ptr_id" = "auth_user"."id") WHERE "app_myuser"."user_ptr_id" IN (10746)
2023-09-06 09:53:55.882 UTC [77] LOG:  duration: 0.297 ms




2023-09-17 07:10:57.719 UTC [296] LOG:  statement: SELECT COUNT(*) FROM ((SELECT "app_postmodel_default"."id" AS "col1", "app_postmodel_default"."author_id" AS "col2", "app_postmodel_default"."body" AS "col3", "app_postmodel_default"."create_at" AS "col4" FROM "app_postmodel_default" WHERE "app_postmodel_default"."author_id" IN (SELECT U0."id" FROM "app_customuser" U0 INNER JOIN "app_followership" U1 ON (U0."id" = U1."to_user_id") WHERE U1."from_user_id" = 330) ORDER BY "app_postmodel_default"."create_at" DESC) UNION (SELECT "app_postmodel_post_partitioned_create_from_2022_to_2023"."id" AS "col1", "app_postmodel_post_partitioned_create_from_2022_to_2023"."author_id" AS "col2", "app_postmodel_post_partitioned_create_from_2022_to_2023"."body" AS "col3", "app_postmodel_post_partitioned_create_from_2022_to_2023"."create_at" AS "col4" FROM "app_postmodel_post_partitioned_create_from_2022_to_2023" WHERE "app_postmodel_post_partitioned_create_from_2022_to_2023"."author_id" IN (SELECT U0."id" FROM "app_customuser" U0 INNER JOIN "app_followership" U1 ON (U0."id" = U1."to_user_id") WHERE U1."from_user_id" = 330) ORDER BY "app_postmodel_post_partitioned_create_from_2022_to_2023"."create_at" DESC)) subquery
2023-09-17 07:10:57.723 UTC [296] LOG:  duration:                         SELECT "app_postmodel_default"."id" AS "col1", "app_postmodel_default"."author_id" AS "col2", "app_postmodel_default"."body" AS "col3", "app_postmodel_default"."create_at" AS "col4" FROM "app_postmodel_default" WHERE "app_postmodel_default"."author_id" IN (SELECT U0."id" FROM "app_customuser" U0 INNER JOIN "app_followership" U1 ON (U0."id" = U1."to_user_id") WHERE U1."from_user_id" = 330) ORDER BY "app_postmodel_default"."create_at" DESC) UNION (SELECT "app_postmodel_post_partitioned_create_from_2022_to_2023"."id" AS "col1", "app_postmodel_post_partitioned_create_from_2022_to_2023"."author_id" AS "col2", "app_postmodel_post_partitioned_create_from_2022_to_2023"."body" AS "col3", "app_postmodel_post_partitioned_create_from_2022_to_2023"."create_at" AS "col4" FROM "app_postmodel_post_partitioned_create_from_2022_to_2023" WHERE "app_postmodel_post_partitioned_create_from_2022_to_2023"."author_id" IN (SELECT U0."id" FROM "app_customuser" U0 INNER JOIN "app_followership" U1 ON (U0."id" = U1."to_user_id") WHERE U1."from_user_id" = 330) ORDER BY "app_postmodel_post_partitioned_create_from_2022_to_2023"."create_at" DESC)) subquery
2023-09-17 07:10:57.725 UTC [296] LOG:  statement: (SELECT "app_postmodel_default"."id" AS "col1", "app_postmodel_default"."author_id" AS "col2", "app_postmodel_default"."body" AS "col3", "app_postmodel_default"."create_at" AS "col4" FROM "app_postmodel_default" WHERE "app_postmodel_default"."author_id" IN (SELECT U0."id" FROM "app_customuser" U0 INNER JOIN "app_followership" U1 ON (U0."id" = U1."to_user_id") WHERE U1."from_user_id" = 330) ORDER BY "app_postmodel_default"."create_at" DESC) UNION (SELECT "app_postmodel_post_partitioned_create_from_2022_to_2023"."id" AS "col1", "app_postmodel_post_partitioned_create_from_2022_to_2023"."author_id" AS "col2", "app_postmodel_post_partitioned_create_from_2022_to_2023"."body" AS "col3", "app_postmodel_post_partitioned_create_from_2022_to_2023"."create_at" AS "col4" FROM "app_postmodel_post_partitioned_create_from_2022_to_2023" WHERE "app_postmodel_post_partitioned_create_from_2022_to_2023"."author_id" IN (SELECT U0."id" FROM "app_customuser" U0 INNER JOIN "app_followership" U1 ON (U0."id" = U1."to_user_id") WHERE U1."from_user_id" = 330) ORDER BY "app_postmodel_post_partitioned_create_from_2022_to_2023"."create_at" DESC) LIMIT 10
2023-09-17 07:10:57.726 UTC [296] LOG:  duration: 1.362 ms
