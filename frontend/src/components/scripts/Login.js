import styles from "../styles/Login.module.css";
import {useState} from 'react';
import axios from 'axios';
import React from 'react';
import {GoogleOAuthProvider, GoogleLogin} from '@react-oauth/google';

const clientId = "708378597417-g4gp2dmet2rarqs4bb6djof4e3kfnu72.apps.googleusercontent.com";


const onSuccess = (response) => {
        // save the token in local storage
        localStorage.setItem('token', response.credential);
        // redirect to home page
        window.location.href = '/home';
    }
;

const onFailure = (response) => {
    console.log('Login Failure:', response);
};


const Login = () => {
    return (
        <div>
            <GoogleOAuthProvider clientId={clientId}>
                <GoogleLogin
                    render={({signIn}) => (
                        <button onClick={signIn}>Login with Google</button>
                    )}
                    onSuccess={onSuccess}
                    onFailure={onFailure}
                />
            </GoogleOAuthProvider>
        </div>

    );
}

export default Login;
