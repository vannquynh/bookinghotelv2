--
-- PostgreSQL database dump
--

\restrict fmlZs5psg0EhhC5z6OBxpfEBNYDtl3h0UZkjbVWodzdIuxv8wZ6RfU60KuWY1ET

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

-- Started on 2026-02-02 11:39:20

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 224 (class 1259 OID 16526)
-- Name: bookings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bookings (
    id integer NOT NULL,
    room_id integer,
    customer_name character varying(100),
    check_in date,
    check_out date,
    total_price integer,
    status character varying(20) DEFAULT 'PENDING'::character varying
);


ALTER TABLE public.bookings OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16525)
-- Name: bookings_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.bookings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bookings_id_seq OWNER TO postgres;

--
-- TOC entry 5038 (class 0 OID 0)
-- Dependencies: 223
-- Name: bookings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.bookings_id_seq OWNED BY public.bookings.id;


--
-- TOC entry 222 (class 1259 OID 16517)
-- Name: rooms; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rooms (
    id integer NOT NULL,
    name character varying(100),
    price integer,
    status character varying(20) DEFAULT 'AVAILABLE'::character varying,
    image_url character varying(255)
);


ALTER TABLE public.rooms OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16516)
-- Name: rooms_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rooms_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.rooms_id_seq OWNER TO postgres;

--
-- TOC entry 5039 (class 0 OID 0)
-- Dependencies: 221
-- Name: rooms_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rooms_id_seq OWNED BY public.rooms.id;


--
-- TOC entry 220 (class 1259 OID 16505)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    password character varying(100) NOT NULL,
    full_name character varying(100),
    role character varying(20) DEFAULT 'user'::character varying
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16504)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 5040 (class 0 OID 0)
-- Dependencies: 219
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 4870 (class 2604 OID 16529)
-- Name: bookings id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookings ALTER COLUMN id SET DEFAULT nextval('public.bookings_id_seq'::regclass);


--
-- TOC entry 4868 (class 2604 OID 16520)
-- Name: rooms id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms ALTER COLUMN id SET DEFAULT nextval('public.rooms_id_seq'::regclass);


--
-- TOC entry 4866 (class 2604 OID 16508)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 5032 (class 0 OID 16526)
-- Dependencies: 224
-- Data for Name: bookings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bookings (id, room_id, customer_name, check_in, check_out, total_price, status) FROM stdin;
1	1	zz	2026-02-02	2026-02-03	500000	PAID
2	1	12	2026-02-03	2026-02-04	500000	PAID
3	1	12	2026-02-04	2026-02-05	500000	PAID
\.


--
-- TOC entry 5030 (class 0 OID 16517)
-- Dependencies: 222
-- Data for Name: rooms; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rooms (id, name, price, status, image_url) FROM stdin;
1	Phòng Standard	500000	AVAILABLE	https://via.placeholder.com/300
3	Phòng VIP	1200000	AVAILABLE	https://via.placeholder.com/300
2	Phòng Deluxe	800000	AVAILABLE	https://via.placeholder.com/300
4	Phòng Tổng Thống	5000000	AVAILABLE	\N
\.


--
-- TOC entry 5028 (class 0 OID 16505)
-- Dependencies: 220
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, password, full_name, role) FROM stdin;
2	12	12	122	user
3	22	1	zz	user
4	admin1	12	ayzz	user
1	admin	1	12	admin
\.


--
-- TOC entry 5041 (class 0 OID 0)
-- Dependencies: 223
-- Name: bookings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.bookings_id_seq', 3, true);


--
-- TOC entry 5042 (class 0 OID 0)
-- Dependencies: 221
-- Name: rooms_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rooms_id_seq', 4, true);


--
-- TOC entry 5043 (class 0 OID 0)
-- Dependencies: 219
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 4, true);


--
-- TOC entry 4879 (class 2606 OID 16533)
-- Name: bookings bookings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookings
    ADD CONSTRAINT bookings_pkey PRIMARY KEY (id);


--
-- TOC entry 4877 (class 2606 OID 16524)
-- Name: rooms rooms_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT rooms_pkey PRIMARY KEY (id);


--
-- TOC entry 4873 (class 2606 OID 16513)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 4875 (class 2606 OID 16515)
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


-- Completed on 2026-02-02 11:39:21

--
-- PostgreSQL database dump complete
--

\unrestrict fmlZs5psg0EhhC5z6OBxpfEBNYDtl3h0UZkjbVWodzdIuxv8wZ6RfU60KuWY1ET

