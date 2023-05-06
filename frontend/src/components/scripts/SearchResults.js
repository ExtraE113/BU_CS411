// displays search results
import React, {useState, useEffect} from 'react';
import styles from "../styles/SearchResults.module.css";
import {Link} from "react-router-dom";
import axios from "axios";
import PodcastCards from "./PodcastCards";

function SearchResults() {
    // get search term passed in from Search.js
    const searchTerm = localStorage.getItem('searchTerm');

    const [searchResults, setSearchResults] = useState([]);
    const token = localStorage.getItem('token');
    // only make one request, check if we've already made a request
    // if we have, don't make another request
    const [requestMade, setRequestMade] = useState(false);
    useEffect(() => {
        if (requestMade) {
            return;
        }
        axios.get(`http://127.0.0.1:8000/podcasts/search?title=${searchTerm}`,
            {
                headers: {
                    Authorization: token,
                }
            }
        ).then(response => {
            setSearchResults(response.data.results);
        }).catch(error => console.log(error)).then(() => {
            setRequestMade(true);
        });
    })

    return (
        <div className={styles.searchResultsWrapper}>
            <h1>Search Results</h1>
            <div className={styles.searchResults}>
                {searchResults.map(podcast => (
                    <div className={styles.searchResult}>
                        <Link to={`/search-results/${podcast.id}`}>
                            <img src={podcast.cover} alt="podcast thumbnail" style={
                                {
                                    maxWidth: "10em"
                                }
                            }/>
                            <h3>{podcast.title}</h3>
                        </Link>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default SearchResults;

