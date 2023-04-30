import styles from "../styles/Navbar.module.css";
import { getAuth } from "firebase/auth";

function NavBar() {
    const auth = getAuth();
    return(
        <nav className = {styles.navbarWrapper}>
            <div className = {styles.logoWrapper}>
                <p>Podcast</p>
            </div>
            <div className = {styles.dashboardWrapper}>
                {/* <p>Hello {auth.currentUser.email}!</p> */}
            </div>
            <div className = {styles.accountWrapper}>
                <p>Search</p>
                <p>Profile</p>
            </div>
        </nav>
    );
}

export default NavBar;