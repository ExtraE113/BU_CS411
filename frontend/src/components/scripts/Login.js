import styles from "../styles/Login.module.css";
import {useState} from 'react';
import axios from 'axios';
import React from 'react';
import {GoogleOAuthProvider, GoogleLogin} from '@react-oauth/google';

const clientId = "708378597417-g4gp2dmet2rarqs4bb6djof4e3kfnu72.apps.googleusercontent.com";


const onSuccess = (response) => {
        console.log(response)
        // Send the `response.tokenObj.id_token` to your Django backend to authenticate the user
        axios.post('http://127.0.0.1:8000/auth/convert-token', {
            token: response.credential
        }).then((response) => {
            console.log(response);
        }).catch((error) => {
            console.log(error);
        });
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
