// search bar component to search for a podcast by name
import React, {useState} from 'react';
import styles from "../styles/Search.module.css";

function Search() {
    const [searchTerm, setSearchTerm] = useState('');
    const token = localStorage.getItem('token');
    const handleChange = event => {
        setSearchTerm(event.target.value);
    };

    const handleSubmit = event => {
        event.preventDefault();
        localStorage.setItem('searchTerm', searchTerm);
        // redirect to search results page
        window.location.href = '/search-results';
    }

    return (
        <div className={styles.searchWrapper}>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Search for a podcast"
                    value={searchTerm}
                    onChange={handleChange}
                />
                <button type="submit">Search</button>
            </form>
        </div>
    );
}

export default Search;