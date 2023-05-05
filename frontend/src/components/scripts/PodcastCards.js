import styles from "../styles/PodcastCards.module.css";
import { useNavigate } from "react-router-dom";
import { useState } from 'react';

function PodcastCards(props) {
    const navigate = useNavigate();

    function watchPodcastHandler() {
        const data = { description: props.data.description, ad: props.data.cuts[0], link: props.data.link };
        navigate("/watch", { state: data });
    }

    return(
        <div className = {styles.titleWrapper}>
            <div className = {styles.cardWrapper} key={props.data.id} onClick = {watchPodcastHandler}>
            </div>
            <p className = {styles.title}>{props.data.title}</p>
        </div>
    );
}

export default PodcastCards;