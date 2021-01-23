import "./styles/ChatApp.css";
import React, {useState} from "react";
import {NetworkManager, Components} from "./react-chatbot-ui";
import 'semantic-ui-css/semantic.min.css'
import {Accordion, Icon, Card, Image, Button, Header, Divider} from 'semantic-ui-react'

function App() {

    const [messages, setMessages] = useState([]);
    const [message, setMessage] = useState(undefined);
    const uid = sessionStorage.getItem("uid");
    const [activeIndex, setActiveIndex] = useState(0);

    const handleClick = (e, titleProps) => {
        const { index } = titleProps
        const newIndex = activeIndex === index ? -1 : index
        setActiveIndex(newIndex);
    }

    return (
        <>
            {!uid?
                <div className={"login-container"}>
                    <label>Insert username and press enter</label>
                    <br />
                    <form>
                        <input
                            className={"input"}
                            type={"text"}
                            onChange={e => sessionStorage.setItem("uid", e.target.value)}
                            placeholder={"Insert your username"}
                        />
                    </form>
                </div> :
                <NetworkManager
                    url={"ws://localhost:8765"}
                    uid={uid}
                    onMessage={(m) => setMessages([...messages, {from: "Chat", message: JSON.parse(m).utterance}])}
                    onOpen={() => setMessages([...messages, {from: "Socket", message: "Connection opened!"}])}
                    onClose={() => setMessages([...messages, {from: "Socket", message: "Connection closed!"}])}
                    onError={() => setMessages([...messages, {from: "Socket", message: "Error in connection!"}])}
                >
                    {/*<div className={"page"}>
                        <div className={"col-left"}>

                        </div>
                        <div className={"col-right"}>
                            <div className={"header"}>
                                <div className='messages' id='messageList'>
                                    <ul>
                                        {messages.map((m, i) => {
                                            return (
                                                <div key={i} className={`message ${m.from}`}>
                                                    <div className='username'>
                                                        {m.from}
                                                    </div>
                                                    <div className='message-body'>
                                                        {m.message}
                                                    </div>
                                                </div>
                                            )
                                        })}
                                    </ul>
                                </div>
                            </div>
                            <footer className={"footer"}>
                                <Components.onSubmit
                                    stopPropagation
                                    type={"utterance"}
                                    payload={{data: message}}
                                    onSend={() => setMessages([...messages, {from: "from-me", message}])}
                                >
                                    <form className={"input-container"}>
                                        <input
                                            className={"input"}
                                            type={"text"}
                                            onChange={e => setMessage(e.target.value)}
                                            placeholder={"Type message"}
                                        />
                                        <button className={"send-button"}>
                                            Send
                                        </button>
                                    </form>

                                </Components.onSubmit>
                            </footer>
                        </div>
                    </div>*/}
                    <div style={{marginTop: 30, display: "flex", justifyContent: "center", alignItems: "center"}}>
                    <Accordion style={{width: 1000}} styled>
                        <Accordion.Title
                            active={activeIndex === 0}
                            index={0}
                            onClick={handleClick}
                        >
                            <Icon name='dropdown' />
                            Choose the item to buy:
                        </Accordion.Title>
                        <Accordion.Content active={activeIndex === 0}>
                            <div style={{
                                flex: 1,
                                flexDirection: "flex-row",
                                display: "flex",
                                justifyContent: "center",
                                alignItems: "center",
                            }}
                            >
                                <Card
                                    onClick={() => setActiveIndex(1)}
                                    style={{margin: 20}}
                                >
                                    <Image src='https://www.supremecommunity.com/u/season/fall-winter2020/sweatshirts/fa32443fd5f342a9801412f5725d38ee_sqr.jpg' wrapped ui={false} />
                                    <Card.Content style={{height: 70}}>
                                        <Card.Header>Cross Box Logo Hooded Sweatshirt</Card.Header>
                                        <Card.Meta>
                                            <span className='date'>Joined in 2015</span>
                                        </Card.Meta>
                                    </Card.Content>
                                    <Card.Content extra>
                                        <a>
                                            <Icon name='check' />
                                            15 pairs available
                                        </a>
                                    </Card.Content>
                                </Card>
                                <Card style={{margin: 20}}>
                                    <Image src='https://www.supremecommunity.com/u/season/fall-winter2020/hats/1a63b0dcba784cce9c14227daf492fe6_sqr.jpg' disabled />
                                    <Card.Content style={{height: 70}}>
                                        <Card.Header>Reactive Print Camp Cap</Card.Header>
                                        <Card.Meta>
                                            <span className='date'>Joined in 2015</span>
                                        </Card.Meta>
                                    </Card.Content>
                                    <Card.Content extra>
                                        <a>
                                            <Icon name='remove' />
                                            Not available in store
                                        </a>
                                    </Card.Content>
                                </Card>
                                <Card
                                    onClick={() => setActiveIndex(1)}
                                    style={{margin: 20}}
                                >
                                    <Image src='https://www.supremecommunity.com/u/season/fall-winter2020/skate/49ca0ec5caa045df82676a0f5fc481cd_sqr.jpg' disabled />
                                    <Card.Content style={{height: 70}}>
                                        <Card.Header>Pills Skateboard</Card.Header>
                                        <Card.Meta>
                                            <span className='date'>Joined in 2015</span>
                                        </Card.Meta>
                                    </Card.Content>
                                    <Card.Content extra>
                                        <a>
                                            <Icon name='remove' />
                                            Not available in store
                                        </a>
                                    </Card.Content>
                                </Card>
                            </div>
                        </Accordion.Content>
                        <Accordion.Title
                            active={activeIndex === 1}
                            index={1}
                            onClick={handleClick}
                        >
                            <Icon name='dropdown' />
                            Set details
                        </Accordion.Title>
                        <Accordion.Content active={activeIndex === 1}>
                            <div style={{flexDirection: "column" , display: "flex", alignItems: "center"}}>
                                <div style={{display: "flex", flexDirection: "row"}}>
                                    <h3 style={{marginRight: 20}}>Choose size</h3>
                                    <Icon name={"cut"}/>
                                </div>
                                <Button.Group>
                                    <Button>Small</Button>
                                    <Button.Or />
                                    <Button>Medium</Button>
                                    <Button.Or />
                                    <Button>Large</Button>
                                </Button.Group>
                                <Divider />
                                <div style={{display: "flex", flexDirection: "row"}}>
                                    <h3 style={{marginRight: 20}}>Choose color</h3>
                                    <Icon name={"paint brush"}/>
                                </div>
                                <Button.Group>
                                    <Button>Navy</Button>
                                    <Button.Or />
                                    <Button>Black</Button>
                                    <Button.Or />
                                    <Button>Large</Button>
                                </Button.Group>
                            </div>
                        </Accordion.Content>

                        <Accordion.Title
                            active={activeIndex === 2}
                            index={2}
                            onClick={handleClick}
                        >
                            <Icon name='dropdown' />
                            How do you acquire a dog?
                        </Accordion.Title>
                        <Accordion.Content active={activeIndex === 2}>
                            <p>
                                Three common ways for a prospective owner to acquire a dog is from
                                pet shops, private owners, or shelters.
                            </p>
                            <p>
                                A pet shop may be the most convenient way to buy a dog. Buying a dog
                                from a private owner allows you to assess the pedigree and
                                upbringing of your dog before choosing to take it home. Lastly,
                                finding your dog from a shelter, helps give a good home to a dog who
                                may not find one so readily.
                            </p>
                        </Accordion.Content>
                        <Accordion.Title
                            active={activeIndex === 3}
                            index={3}
                            onClick={handleClick}
                        >
                            <Icon name='dropdown' />
                            How do you acquire a dog?
                        </Accordion.Title>
                        <Accordion.Content active={activeIndex === 3}>
                            <p>
                                Three common ways for a prospective owner to acquire a dog is from
                                pet shops, private owners, or shelters.
                            </p>
                            <p>
                                A pet shop may be the most convenient way to buy a dog. Buying a dog
                                from a private owner allows you to assess the pedigree and
                                upbringing of your dog before choosing to take it home. Lastly,
                                finding your dog from a shelter, helps give a good home to a dog who
                                may not find one so readily.
                            </p>
                        </Accordion.Content>
                    </Accordion>
                </div>
                </NetworkManager>
            }
        </>
    );
}

export default App;




