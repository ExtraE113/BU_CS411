import { useLocation } from 'react-router-dom';
import React, { useState, useRef } from "react";
import styles from "../styles/Watch.module.css";

function Watch() {
    const location = useLocation();
    const data = location.state;
    const adStart = data.ad[0]; // Timestamp for adStart in seconds
    const adEnd = data.ad[1]; // Timestamp for adEnd in seconds
    const videoRef = useRef(null);
    const [adBlockerEnabled, setAdBlockerEnabled] = useState(true);

    const handleTimeUpdate = () => {
        if (!adBlockerEnabled) {
            return; // Don't skip ads if the ad-blocker is disabled
        }
        const currentTime = videoRef.current.currentTime;
        if (currentTime >= adStart && currentTime < adEnd) {
          videoRef.current.currentTime = adEnd;
        }
    };

    const handleToggleAds = () => {
        setAdBlockerEnabled(!adBlockerEnabled);
    }

    const descriptionWithoutTags = data.description.replace(/(<([^>]+)>)/gi, '');

    return(
        <div className = {styles.videoWrapper}>
            <video src={data.link} controls ref={videoRef} onTimeUpdate={handleTimeUpdate}>
                Your browser does not support the video tag.
            </video>
            <p className = {styles.description}>{descriptionWithoutTags}</p>
            <label htmlFor="toggle-ads">There is an ad from {data.ad[0]} to {data.ad[1]} seconds. Enable ad-blocker?</label>
            <input type="checkbox" id="toggle-ads" checked={adBlockerEnabled} onChange={handleToggleAds} />
        </div>

    );
}

export default Watch;