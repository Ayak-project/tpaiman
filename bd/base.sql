-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

CREATE TABLE public.files (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  name text NOT NULL,
  link text NOT NULL,
  status text NOT NULL CHECK (status = ANY (ARRAY['private'::text, 'public'::text])),
  user_id uuid,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT files_pkey PRIMARY KEY (id),
  CONSTRAINT files_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id)
);
CREATE TABLE public.users (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  name text NOT NULL,
  email text NOT NULL UNIQUE,
  password text NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT users_pkey PRIMARY KEY (id)
);