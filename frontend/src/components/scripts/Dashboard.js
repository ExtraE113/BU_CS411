import styles from "../styles/Dashboard.module.css";
import React, {useEffect, useState} from 'react';
import PodcastCards from "./PodcastCards";

function Dashboard() {
    const [podcasts, setPodcasts] = useState(null);
    const [user, setUser] = useState([]);

    useEffect(() => {
        // set the authorization header from the token in local storage
        const token = localStorage.getItem('token');
        fetch("http://127.0.0.1:8000/episodes/26/",
            {
                headers: {
                    Authorization: token,
                }
            })
            .then(response => response.json())
            .then(data => setPodcasts(data))
            .catch(error => console.log(error));
    }, []);

    if (podcasts === null) {
        return <div className = {styles.loading}>Loading...</div>;
    }
    console.log(podcasts);
    return (
        <section>
            <h1 className={styles.favorites}>My Favorites</h1>
            <div className = {styles.wrapper}>
                <div>
                    <PodcastCards data={podcasts}/>
                </div>
                <button className={styles.addPodcastBtn}>Add Podcast</button>
            </div>
        </section>
    );
}

export default Dashboard;