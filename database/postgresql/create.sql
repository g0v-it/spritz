
--
-- Name: guarantor; Type: TABLE; Schema: public; Owner: dinogen
--

CREATE TABLE public.guarantor (
    votation_id integer NOT NULL,
    user_id integer NOT NULL,
    passphrase_ok integer NOT NULL,
    hash_ok integer NOT NULL,
    order_n integer
);


--
-- Name: votation; Type: TABLE; Schema: public; Owner: dinogen
--

CREATE TABLE public.votation (
    votation_id integer NOT NULL,
    promoter_user_id integer NOT NULL,
    votation_description text NOT NULL,
    begin_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone NOT NULL,
    votation_type text NOT NULL,
    votation_status integer NOT NULL
);




--
-- Name: vote; Type: TABLE; Schema: public; Owner: dinogen
--

CREATE TABLE public.vote (
    vote_key text NOT NULL,
    votation_id integer NOT NULL,
    option_id integer NOT NULL,
    jud_value integer
);



--
-- Name: voter; Type: TABLE; Schema: public; Owner: dinogen
--

CREATE TABLE public.voter (
    user_id integer NOT NULL,
    votation_id integer NOT NULL
);



--
-- Name: voting_option; Type: TABLE; Schema: public; Owner: dinogen
--

CREATE TABLE public.voting_option (
    option_id integer NOT NULL,
    votation_id integer,
    option_name text,
    description text
);







--
-- Name: voting_user; Type: TABLE; Schema: public; Owner: dinogen
--



ALTER TABLE ONLY public.votation ALTER COLUMN votation_id SET DEFAULT nextval('public.votation_votation_id_seq'::regclass);


--
-- Name: voting_option option_id; Type: DEFAULT; Schema: public; Owner: dinogen
--

ALTER TABLE ONLY public.voting_option ALTER COLUMN option_id SET DEFAULT nextval('public.voting_option_option_id_seq'::regclass);


--
-- Name: voting_user user_id; Type: DEFAULT; Schema: public; Owner: dinogen
--

ALTER TABLE ONLY public.voting_user ALTER COLUMN user_id SET DEFAULT nextval('public.voting_user_user_id_seq'::regclass);




--
-- Data for Name: votation; Type: TABLE DATA; Schema: public; Owner: dinogen
--


ALTER TABLE ONLY public.guarantor
    ADD CONSTRAINT guarantor_pkey PRIMARY KEY (votation_id, user_id);


--
-- Name: votation votation_pkey; Type: CONSTRAINT; Schema: public; Owner: dinogen
--

ALTER TABLE ONLY public.votation
    ADD CONSTRAINT votation_pkey PRIMARY KEY (votation_id);


--
-- Name: votation votation_votation_description_key; Type: CONSTRAINT; Schema: public; Owner: dinogen
--

ALTER TABLE ONLY public.votation
    ADD CONSTRAINT votation_votation_description_key UNIQUE (votation_description);


--
-- Name: vote vote_pkey; Type: CONSTRAINT; Schema: public; Owner: dinogen
--

ALTER TABLE ONLY public.vote
    ADD CONSTRAINT vote_pkey PRIMARY KEY (vote_key, votation_id, option_id);


--
-- Name: voter voter_pkey; Type: CONSTRAINT; Schema: public; Owner: dinogen
--

ALTER TABLE ONLY public.voter
    ADD CONSTRAINT voter_pkey PRIMARY KEY (user_id, votation_id);


--
-- Name: voting_judgement voting_judgement_pkey; Type: CONSTRAINT; Schema: public; Owner: dinogen
--

ALTER TABLE ONLY public.voting_judgement
    ADD CONSTRAINT voting_judgement_pkey PRIMARY KEY (votation_id, jud_value);


--
-- Name: voting_option voting_option_pkey; Type: CONSTRAINT; Schema: public; Owner: dinogen
--

ALTER TABLE ONLY public.voting_option
    ADD CONSTRAINT voting_option_pkey PRIMARY KEY (option_id);


--
-- Name: voting_option voting_option_votation_id_option_name_key; Type: CONSTRAINT; Schema: public; Owner: dinogen
--

ALTER TABLE ONLY public.voting_option
    ADD CONSTRAINT voting_option_votation_id_option_name_key UNIQUE (votation_id, option_name);


--
-- Name: voting_user voting_user_pkey; Type: CONSTRAINT; Schema: public; Owner: dinogen
--

ALTER TABLE ONLY public.voting_user
    ADD CONSTRAINT voting_user_pkey PRIMARY KEY (user_id);


--
-- Name: voting_user voting_user_user_name_key; Type: CONSTRAINT; Schema: public; Owner: dinogen
--

ALTER TABLE ONLY public.voting_user
    ADD CONSTRAINT voting_user_user_name_key UNIQUE (user_name);


--
-- PostgreSQL database dump complete
--

