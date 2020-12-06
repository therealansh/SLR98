import React, { useState } from 'react'
import { useSpeechSynthesis } from 'react-speech-kit';
import Axios from 'axios'
import "./VideoFrame.css"
import Webcam from "react-webcam"

export default function VideoFrame({custom}) {
    const videoConstraints = {
        width: 800,
        height: 450,
        facingMode: "user"
      };
    
    return (
        <>
            <div className="vid-frame">
                <div className="vid">
                    <img id="bg" width="800px" height="450px" src={custom ? "http://0.0.0.0:5000/custom_frame" : "http://0.0.0.0:5000/video_feed"} ></img>
                </div>
            </div>
        </>
    ) 
}
