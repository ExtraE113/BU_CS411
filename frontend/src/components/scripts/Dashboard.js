import styles from "../styles/Dashboard.module.css";
import {db} from "../../firebase";
import {doc, setDoc} from "firebase/firestore";
import React, {useEffect, useState} from 'react';
import {getAuth} from "firebase/auth";
import {getFirestore, getDoc} from "firebase/firestore";
import PodcastCards from "./PodcastCards";

// import axios from "axios";

function Dashboard() {
    const [podcasts, setPodcasts] = useState(null);
    const [user, setUser] = useState([]);

    useEffect(() => {
        // set the authorization header from the token in local storage
        const token = localStorage.getItem('token');
        fetch("http://127.0.0.1:8000/podcasts/",
            {
                headers: {
                    Authorization: token,
                }
            })
            .then(response => response.json())
            .then(data => setPodcasts(data))
            .catch(error => console.log(error));
    }, []);

    //Axios has some issues as it returns a HTML static file instead of JSON format
//   useEffect(() => {
//     axios
//       .get("http://127.0.0.1:8000/podcasts/?format=api")
//       .then(response => {
//         setPodcasts(response.JSON);
//       })
//       .catch(error => {
//         console.log(error);
//       });
//   }, []);

    // useEffect(() => {
    //     const auth = getAuth();
    //     const loggedUser = auth.onAuthStateChanged(async (user) => {
    //     if (user) {
    //         setUser(user);
    //         setDoc(doc(db, "users", user.uid), {
    //             email: user.email
    //         });
    //     } else {
    //         setUser(null);
    //     }
    //     });
    //     return () => loggedUser();
    // }, []);

    if (podcasts === null) {
        return <div>Loading...</div>;
    }

    return (
        <section>
            <h1 className={styles.favorites}>My Favorites</h1>
            {/*<div>*/}
            {/*    {podcasts && podcasts.map(podcast => (*/}
            {/*        <PodcastCards data={podcast}/>*/}
            {/*    ))}*/}
            {/*</div>*/}
            <button className={styles.addPodcastBtn}>Add Podcast</button>
        </section>
    );
}

export default Dashboard;