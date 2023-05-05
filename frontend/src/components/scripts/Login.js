import axios from "axios";
import {Navigate} from "react-router-dom";
import {useState} from "react";
import GoogleLogin from "react-google-login";
import {gapi} from "gapi-script";
import {useEffect} from "react";
import 'bootstrap/dist/css/bootstrap.css';

export const Login = () => {
    const client_id = '708378597417-g4gp2dmet2rarqs4bb6djof4e3kfnu72.apps.googleusercontent.com';

    const onSuccess = async (res) => {
        console.log('succzddgsfgess:', res.accessToken);
        const user = {
            "grant_type":"convert_token",
            "client_id": client_id,
            "client_secret": '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',
            "backend":"google-oauth2",
            "token": res.accessToken
        };
        //console.log(user)
        const {data} = await axios.post('http://127.0.0.1:8000/auth/convert-token', user ,{headers: {
            'Content-Type': 'application/json'
        }}, {withCredentials: true});

        //console.log(data, data['access_token'])
        axios.defaults.headers.common['Authorization'] = `Bearer ${data['access_token']}`;
        localStorage.clear();
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('refresh_token', data.refresh_token);
        window.location.href = '/'

        // const onFailure = (err) => {
        //     console.log('failed:', err);
        // };
    }
    
    return(
        <div className="Auth-form-container">
          <GoogleLogin
            clientId={client_id}
            buttonText="Sign in with Google"
            onSuccess={onSuccess}
            cookiePolicy={'single_host_origin'}
            />
        </div>
    )
}