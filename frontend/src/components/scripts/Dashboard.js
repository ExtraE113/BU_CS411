import styles from "../styles/Dashboard.module.css";
import { db } from "../../firebase";
import { doc, setDoc } from "firebase/firestore"; 
import React, { useEffect, useState } from 'react';
import { getAuth } from "firebase/auth";
import { getFirestore, getDoc } from "firebase/firestore";

function Dashboard() {
    const [podcasts, setPodcasts] = useState(null);
    const [user, setUser] = useState([]);

    useEffect(() => {
        const auth = getAuth();
        const loggedUser = auth.onAuthStateChanged(async (user) => {
        if (user) {
            setUser(user);
            setDoc(doc(db, "users", user.uid), {
                email: user.email
            });
        } else {
            setUser(null);
        }
        });
        return () => loggedUser();
    }, []);

    return(
        <section>
            <h1 className = {styles.favorites}>My Favorites</h1>
            <button className = {styles.addPodcastBtn}>Add Podcast</button>
        </section>
    );
}

export default Dashboard;