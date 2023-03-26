-- this file was manually created
INSERT INTO public.users (display_name, email, handle, cognito_user_id)
VALUES
  ('sadaf','smbaig251@gmail.com', 'sadaf_23','117eb7d2-d93b-484b-8af0-62f69ff106f5'),
  ('Andrew Bayko','bayko@exampro.co', 'bayko','MOCK'),
  ('Londo Mollari','lmollari@centari.com','londo','MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'sadaf_23' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  )