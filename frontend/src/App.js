import './App.css';
import {BrowserRouter, Routes, Route} from 'react-router-dom';
import {Login} from "../src/components/scripts/Login";
import {Home} from "../src/components/scripts/Home";
import {Navigation} from "../src/components/scripts/Navigations";
import {Logout} from "../src/components/scripts/Logout";

function App() {
    return <BrowserRouter>
    <Navigation></Navigation>
        <Routes>
            <Route path="/" element={<Home/>}/>
            <Route path="/login" element={<Login/>}/>
            <Route path="/logout" element={<Logout/>}/>
        </Routes>
    </BrowserRouter>;
}

export default App;
