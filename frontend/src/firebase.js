import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getFirestore } from "firebase/firestore";
import { getAuth } from "firebase/auth";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCArrM4H8wucuhKL7t6-zQRXzspMrpTdps",
  authDomain: "podcast-adblocker.firebaseapp.com",
  projectId: "podcast-adblocker",
  storageBucket: "podcast-adblocker.appspot.com",
  messagingSenderId: "817213660031",
  appId: "1:817213660031:web:0c807810feb4f32bac584a",
  measurementId: "G-Z40ZMZM04P"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
export const auth = getAuth(app);
export const db = getFirestore(app);