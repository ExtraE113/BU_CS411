import './App.css';
import { BrowserRouter,Routes,Route,Link } from "react-router-dom";
import NavBar from './components/scripts/Navbar';
import Login from './components/scripts/Login';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element = {<Login />} />
        <Route path="/home" element = {<NavBar />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
