ALTER TABLE public.votation
ADD COLUMN description_url text NOT NULL;

ALTER TABLE public.voter
ADD COLUMN voted integer NOT NULL default 0;
