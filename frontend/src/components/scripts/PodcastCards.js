import styles from "../styles/PodcastCards.module.css";

function PodcastCards(props) {
    return(
        <div className = {styles.cardWrapper} key={props.data.id}>
            <p>{props.data.category}</p>
            <p>{props.data.description}</p>
            {/* <p>{props.data.rss_feed_url}</p> */}
            <p className = {styles.title}>{props.data.title}</p>
        </div>
    );
}

export default PodcastCards;