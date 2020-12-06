import React, { useState } from 'react'
import { useSpeechSynthesis } from 'react-speech-kit';
import Axios from 'axios'
import { Navbar,Container,Row,Col,Card } from 'react-bootstrap'
import "./aslPredict.css"
import ArrowForwardIosIcon from '@material-ui/icons/ArrowForwardIos';
import VideoFrame from './VideoFrame'
import {Link} from 'react-router-dom';

export default function CustomPredict() {
    const [predicted,setPredict] = useState('')
    const { speak } = useSpeechSynthesis();

    function predictFrame() {
        Axios.get("http://0.0.0.:5000/custom").then((res)=>{setPredict(res.data);speak({text:`${res.data}`})})
    }

    return (
        <>
        <Navbar fixed="top" variant="light" style={{margin:"1.5rem"}}>
            <Navbar.Collapse className="justify-content-end"><Link to="/customTrainer"><button><ArrowForwardIosIcon /></button></Link></Navbar.Collapse>
        </Navbar>
            <div style={{marginTop:"auto",marginBottom:"auto", display:"flex",justifyContent:"space-evenly"}}>
            <Row>
                <Col>
                    <VideoFrame custom={true}/>
                </Col>
                <Col>
                <div className="predict-card">
                    <p>Prediction: {predicted}</p>
                    <button onClick={predictFrame}>Predict</button>
                </div>
                </Col>
            </Row>
            </div>
        </>
    )
}
