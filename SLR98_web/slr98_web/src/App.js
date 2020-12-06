import logo from './logo.svg';
import './App.css';
import LandingPage from './components/LandingPage'
import ASLPredict from './components/ASLPredict'
import { Navbar,Container,Row,Col } from 'react-bootstrap'
import { Switch, BrowserRouter as Router, Route,Link } from 'react-router-dom'
import CustomPredict from './components/CustomGesture';

function App() {
  return (
    <Router>
      <Navbar fixed="top" variant="light">
                <Navbar.Brand><Link to="/"><button>SLR</button></Link></Navbar.Brand>
            </Navbar>
      <div className="App">
        <div className="wrapper">
          
          <Switch>
            <Route exact path="/" component={LandingPage}/>
            <Route path="/asl" component={ASLPredict} />
            
            <Route path="/custom" component={CustomPredict} />
          </Switch>
          
        </div>
      </div>
    </Router>
  );
}

export default App;
