ALTER TABLE public.votation
ADD COLUMN description_url text NOT NULL default '';

ALTER TABLE public.voter
ADD COLUMN voted integer NOT NULL default 0;
