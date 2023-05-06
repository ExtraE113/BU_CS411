import styles from "../styles/Navbar.module.css";
import Search from "./Search";

function NavBar() {
    return (
        <nav className={styles.navbarWrapper}>
            <div className={styles.logoWrapper}>
                <p>Podcast</p>
            </div>
            <div className={styles.dashboardWrapper}>
                {/* <p>Hello {auth.currentUser.email}!</p> */}
            </div>
            <div className={styles.accountWrapper}>
                {/*Search*/}
                <Search/>
            </div>
        </nav>
    );
}

export default NavBar;