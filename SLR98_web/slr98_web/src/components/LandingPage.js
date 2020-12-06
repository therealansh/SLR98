import React from 'react'
import { Navbar,Container,Row,Col } from 'react-bootstrap'
import './LandingPage.css'
import TypeWriter from 'typewriter-effect';
import Fade from 'react-reveal/Fade';
import {Link} from 'react-router-dom'

export default function LandingPage() {
    return (
        <>
            
            <div className="centered">
                <Row>
                    <div className="typer">
                        <TypeWriter 
                            options={{
                              strings:['Speak.',"Listen.","Connect."],
                              autoStart:true,
                              loop:true,
                          }} />
                    </div>
                    <div >
                        <Fade right>
                              <div>
                                  <Link to={'/asl'}>
                                      <button>Start</button>
                                  </Link>
                              </div>
                          </Fade>
                    </div>
                </Row>
            </div>
        </>
    )
}
