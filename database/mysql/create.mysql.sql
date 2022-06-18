--
-- Name: judgement; Type: TABLE; Schema: public; Owner: dinogen
--

CREATE TABLE judgement (
    votation_id integer NOT NULL,
    jud_value integer NOT NULL,
    jud_name VARCHAR(50) NOT NULL,
    PRIMARY KEY (votation_id, jud_value)
);



--
-- Name: option; Type: TABLE; Schema: public; Owner: dinogen
--

CREATE TABLE `option` (
    option_id integer NOT NULL primary key auto_increment,
    votation_id integer,
    option_name VARCHAR(50) NOT NULL
);


--
-- Name: votation; Type: TABLE; Schema: public; Owner: dinogen
--

CREATE TABLE votation (
    votation_id integer NOT NULL primary key auto_increment,
    promoter_user_id integer,
    votation_description VARCHAR(500) NOT NULL,
    description_url VARCHAR(500) NOT NULL,
    begin_date DATETIME NOT NULL,
    end_date DATETIME NOT NULL,
    votation_type VARCHAR(10) NOT NULL,
    votation_status integer NOT NULL,
    list_voters integer NOT NULL
);





--
-- Name: vote; Type: TABLE; Schema: public; Owner: dinogen
--

CREATE TABLE vote (
    vote_key VARCHAR(128) NOT NULL,
    votation_id integer NOT NULL,
    option_id integer NOT NULL,
    jud_value integer NOT NULL,
    PRIMARY KEY (vote_key, votation_id, option_id)
);



--
-- Name: voter; Type: TABLE; Schema: public; Owner: dinogen
--

CREATE TABLE voter (
    user_id integer NOT NULL,
    votation_id integer NOT NULL,
    voted integer, 
    PRIMARY KEY (user_id, votation_id)
);



--
-- Name: votinguser; Type: TABLE; Schema: public; Owner: dinogen
--

CREATE TABLE votinguser (
    user_id integer NOT NULL primary key auto_increment,
    user_name VARCHAR(200) NOT NULL,
    pass_word VARCHAR(200) NOT NULL,
    email VARCHAR(200),
    verified integer
);




--
-- Name: votation votation_votation_description_key; Type: CONSTRAINT; Schema: public; Owner: dinogen
--

ALTER TABLE  votation
    ADD CONSTRAINT votation_votation_description_key UNIQUE (votation_description);






--
-- Name: votinguser votinguser_user_name_key; Type: CONSTRAINT; Schema: public; Owner: dinogen
--

ALTER TABLE  votinguser
    ADD CONSTRAINT votinguser_user_name_key UNIQUE (user_name);


--
-- Name: judgement judgement_votation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dinogen
--

ALTER TABLE  judgement
    ADD CONSTRAINT judgement_votation_id_fkey FOREIGN KEY (votation_id) REFERENCES votation(votation_id);


--
-- Name: option option_votation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dinogen
--

ALTER TABLE  `option`
    ADD CONSTRAINT option_votation_id_fkey FOREIGN KEY (votation_id) REFERENCES votation(votation_id);


--
-- Name: votation votation_promoter_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dinogen
--

ALTER TABLE  votation
    ADD CONSTRAINT votation_promoter_user_id_fkey FOREIGN KEY (promoter_user_id) REFERENCES votinguser(user_id);


--
-- Name: vote vote_option_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dinogen
--

ALTER TABLE  vote
    ADD CONSTRAINT vote_option_id_fkey FOREIGN KEY (option_id) REFERENCES `option`(option_id);


--
-- Name: vote vote_votation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dinogen
--

ALTER TABLE  vote
    ADD CONSTRAINT vote_votation_id_fkey FOREIGN KEY (votation_id) REFERENCES votation(votation_id);


--
-- Name: voter voter_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dinogen
--

ALTER TABLE  voter
    ADD CONSTRAINT voter_user_id_fkey FOREIGN KEY (user_id) REFERENCES votinguser(user_id);


--
-- Name: voter voter_votation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dinogen
--

ALTER TABLE  voter
    ADD CONSTRAINT voter_votation_id_fkey FOREIGN KEY (votation_id) REFERENCES votation(votation_id);


--
-- users for test pourpose
--
insert into  votinguser(user_id,user_name,pass_word,email,verified) values (0,'aldo','aldo','',1);
insert into  votinguser(user_id,user_name,pass_word,email,verified) values (1,'beppe','beppe','',1);
insert into  votinguser(user_id,user_name,pass_word,email,verified) values (2,'carlo','carlo','',1);
insert into  votinguser(user_id,user_name,pass_word,email,verified) values (3,'dario','dario','',1);
insert into  votinguser(user_id,user_name,pass_word,email,verified) values (4,'ezio','ezio','',1);

