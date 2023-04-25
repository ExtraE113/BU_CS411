import styles from "../styles/Login.module.css";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword, getUserByEmail } from "firebase/auth";
import { auth, db } from "../../firebase";

function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const signIn = e => {
        e.preventDefault();

        const auth = getAuth();
        signInWithEmailAndPassword(auth, email, password)
        .then(auth => {
            navigate("/home");
        })
        .catch(error => alert(error.message))
    }

    const createAccount = e => {
        e.preventDefault();
        
        const auth = getAuth();
        createUserWithEmailAndPassword(auth, email, password)
        .then((auth) => {
            if (auth) {
                navigate("/home");
            }
        })
        .catch(error => alert(error.message))
    }

    return (
        <section className = {styles.login}>
            <div>
                <h1>Podcast</h1>
                <form>
                    <div className = {styles.emailInput}>
                        <h4 className= {styles.logo3}> Email</h4>
                        <input type = "text" value = {email} onChange = {e => {setEmail(e.target.value)}} className = {styles.email}/>
                    </div>
                    <div className = {styles.passwordInput}>
                        <h4 className= {styles.logo3}> Password</h4>
                        <input type = "password" value = {password} onChange = {e => {setPassword(e.target.value)}} className = {styles.password} />
                    </div>

                    <button type = "submit" onClick = {signIn} className = {styles.signInBtn}>Sign In</button>
                </form>

                <p className = {styles.message}>Don't have an account? Create one here!</p>
                <button className = {styles.createAccBtn} onClick = {createAccount}>Create your account</button>
            </div>
        </section>
    );
}

export default Login;