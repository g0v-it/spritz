--
-- PostgreSQL database dump
--

-- Dumped from database version 11.1
-- Dumped by pg_dump version 11.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

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


ALTER TABLE public.guarantor OWNER TO dinogen;

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


ALTER TABLE public.votation OWNER TO dinogen;

--
-- Name: votation_votation_id_seq; Type: SEQUENCE; Schema: public; Owner: dinogen
--

CREATE SEQUENCE public.votation_votation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.votation_votation_id_seq OWNER TO dinogen;

--
-- Name: votation_votation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dinogen
--

ALTER SEQUENCE public.votation_votation_id_seq OWNED BY public.votation.votation_id;


--
-- Name: vote; Type: TABLE; Schema: public; Owner: dinogen
--

CREATE TABLE public.vote (
    vote_key text NOT NULL,
    votation_id integer NOT NULL,
    option_id integer NOT NULL,
    jud_value integer
);


ALTER TABLE public.vote OWNER TO dinogen;

--
-- Name: voter; Type: TABLE; Schema: public; Owner: dinogen
--

CREATE TABLE public.voter (
    user_id integer NOT NULL,
    votation_id integer NOT NULL
);


ALTER TABLE public.voter OWNER TO dinogen;

--
-- Name: voting_judgement; Type: TABLE; Schema: public; Owner: dinogen
--

CREATE TABLE public.voting_judgement (
    votation_id integer NOT NULL,
    jud_value integer NOT NULL,
    jud_name text,
    description text
);


ALTER TABLE public.voting_judgement OWNER TO dinogen;

--
-- Name: voting_option; Type: TABLE; Schema: public; Owner: dinogen
--

CREATE TABLE public.voting_option (
    option_id integer NOT NULL,
    votation_id integer,
    option_name text,
    description text
);


ALTER TABLE public.voting_option OWNER TO dinogen;

--
-- Name: voting_option_option_id_seq; Type: SEQUENCE; Schema: public; Owner: dinogen
--

CREATE SEQUENCE public.voting_option_option_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.voting_option_option_id_seq OWNER TO dinogen;

--
-- Name: voting_option_option_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dinogen
--

ALTER SEQUENCE public.voting_option_option_id_seq OWNED BY public.voting_option.option_id;


--
-- Name: voting_user; Type: TABLE; Schema: public; Owner: dinogen
--

CREATE TABLE public.voting_user (
    user_id integer NOT NULL,
    user_name text NOT NULL,
    pass_word text NOT NULL
);


ALTER TABLE public.voting_user OWNER TO dinogen;

--
-- Name: voting_user_user_id_seq; Type: SEQUENCE; Schema: public; Owner: dinogen
--

CREATE SEQUENCE public.voting_user_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.voting_user_user_id_seq OWNER TO dinogen;

--
-- Name: voting_user_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dinogen
--

ALTER SEQUENCE public.voting_user_user_id_seq OWNED BY public.voting_user.user_id;


--
-- Name: votation votation_id; Type: DEFAULT; Schema: public; Owner: dinogen
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
-- Data for Name: guarantor; Type: TABLE DATA; Schema: public; Owner: dinogen
--

COPY public.guarantor (votation_id, user_id, passphrase_ok, hash_ok, order_n) FROM stdin;
\.


--
-- Data for Name: votation; Type: TABLE DATA; Schema: public; Owner: dinogen
--

COPY public.votation (votation_id, promoter_user_id, votation_description, begin_date, end_date, votation_type, votation_status) FROM stdin;
1	1	Miglior vino	2018-12-18 12:00:00	2018-12-25 12:00:00	maj_jud	1
2	2	Film per tutti	2018-12-18 12:00:00	2018-12-19 12:00:00	maj_jud	1
\.


--
-- Data for Name: vote; Type: TABLE DATA; Schema: public; Owner: dinogen
--

COPY public.vote (vote_key, votation_id, option_id, jud_value) FROM stdin;
96c698f17439b48a8fd9af3402a547a7eef468cd56bed461d447204fc84471a0	2	6	5
96c698f17439b48a8fd9af3402a547a7eef468cd56bed461d447204fc84471a0	2	7	4
96c698f17439b48a8fd9af3402a547a7eef468cd56bed461d447204fc84471a0	2	8	5
96c698f17439b48a8fd9af3402a547a7eef468cd56bed461d447204fc84471a0	2	9	1
96c698f17439b48a8fd9af3402a547a7eef468cd56bed461d447204fc84471a0	2	10	4
96c698f17439b48a8fd9af3402a547a7eef468cd56bed461d447204fc84471a0	2	11	5
96c698f17439b48a8fd9af3402a547a7eef468cd56bed461d447204fc84471a0	2	12	5
\.


--
-- Data for Name: voter; Type: TABLE DATA; Schema: public; Owner: dinogen
--

COPY public.voter (user_id, votation_id) FROM stdin;
2	2
\.


--
-- Data for Name: voting_judgement; Type: TABLE DATA; Schema: public; Owner: dinogen
--

COPY public.voting_judgement (votation_id, jud_value, jud_name, description) FROM stdin;
\.


--
-- Data for Name: voting_option; Type: TABLE DATA; Schema: public; Owner: dinogen
--

COPY public.voting_option (option_id, votation_id, option_name, description) FROM stdin;
1	1	BIANCO	
2	1	PROSECCO	
3	1	ROSATO	
4	1	ROSSO	
5	1	SPUMANTE	
6	2	BARBIE LA PRINCIPESSA E LA POVERA	
7	2	CARS	
8	2	GLI INCREDIBILI	
9	2	LE 12 PRINCIPESSE DANZANTI	
10	2	MONSTERS E CO	
11	2	RATATOUILLE	
12	2	TOY STORY	
\.


--
-- Data for Name: voting_user; Type: TABLE DATA; Schema: public; Owner: dinogen
--

COPY public.voting_user (user_id, user_name, pass_word) FROM stdin;
1	aldo	aldo
2	beppe	beppe
3	carlo	carlo
4	dario	dario
5	ernesto	ernesto
6	fabio	fabio
7	dinogen	a
8	tommaso	a
9	giada	a
10	francesca	a
11	roberta	a
\.


--
-- Name: votation_votation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dinogen
--

SELECT pg_catalog.setval('public.votation_votation_id_seq', 2, true);


--
-- Name: voting_option_option_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dinogen
--

SELECT pg_catalog.setval('public.voting_option_option_id_seq', 12, true);


--
-- Name: voting_user_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dinogen
--

SELECT pg_catalog.setval('public.voting_user_user_id_seq', 11, true);


--
-- Name: guarantor guarantor_pkey; Type: CONSTRAINT; Schema: public; Owner: dinogen
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

