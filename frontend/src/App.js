import "./styles/ChatApp.css";
import React, {useState} from "react";
import {NetworkManager} from "./react-chatbot-ui";
import 'semantic-ui-css/semantic.min.css'
import {Accordion, Icon, Card, Image, Button, Label, Divider} from 'semantic-ui-react'
import {ChatComponent} from "./components/ChatComponent";

function App() {

    const [messages, setMessages] = useState([]);
    const [message, setMessage] = useState(undefined);
    const uid = sessionStorage.getItem("uid");
    const [activeIndex, setActiveIndex] = useState(0);
    const [choice, setChoice] = useState(0);

    const handleClick = (e, titleProps) => {
        const { index } = titleProps
        const newIndex = activeIndex === index ? -1 : index
        setActiveIndex(newIndex);
    }

    const data = [
        {
            source: "https://www.supremecommunity.com/u/season/fall-winter2020/sweatshirts/fa32443fd5f342a9801412f5725d38ee_sqr.jpg",
            name: "Cross Box Logo Hooded Sweatshirt",
            availability: 15,
            sizes: ["Small", "Medium", "Large"],
            colors: [
                {
                    source: "https://www.supremecommunity.com/u/season/fall-winter2020/sweatshirts/details/9d39875acfc240cb998112c6d3ed487d_sqr.jpg",
                    color: "gray",
                    name: "Heather Grey",
                },
                {
                    source: "https://www.supremecommunity.com/u/season/add/202012033aa47654094d4deb8df2cf28ccd37b17_sqr.jpg",
                    color: "black",
                    name: "Black",
                },
                {
                    source: "https://www.supremecommunity.com/u/season/add/20201203017859abdba3487da8e720fb11ac402b_sqr.jpg",
                    color: "violet",
                    name: "Purple",
                },
            ]
        },
        {
            source: "https://www.supremecommunity.com/u/season/fall-winter2020/hats/1a63b0dcba784cce9c14227daf492fe6_sqr.jpg",
            name: "Reactive Print Camp Cap",
            availability: 0,
        },
        {
            source: "https://www.supremecommunity.com/u/season/fall-winter2020/skate/49ca0ec5caa045df82676a0f5fc481cd_sqr.jpg",
            name: "Pills Skateboard",
            availability: 0,
        },
    ]

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
                                {data.map((item, index) => {
                                    return (
                                        <Card
                                            onClick={() => {
                                                if (item.availability) {
                                                    setActiveIndex(1);
                                                    setChoice(index);
                                                }
                                            }}
                                            style={{margin: 20}}
                                        >
                                            <Image src={item.source} disabled={!item.availability} style={{margin: 10}}/>
                                            <Card.Content style={{height: 70}}>
                                                <Card.Header>{item.name}</Card.Header>
                                            </Card.Content>
                                            <Card.Content extra>
                                                <Icon name={item.availability? 'check' : "remove"} />
                                                {item.availability || "No"} pairs available
                                            </Card.Content>
                                        </Card>
                                    );
                                })}
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
                                <div style={{
                                    flex: 1,
                                    flexDirection: "flex-row",
                                    display: "flex",
                                    justifyContent: "center",
                                    alignItems: "center",
                                }}
                                >
                                    {data[choice].colors.map((color, index) => {
                                        return (
                                            <Card
                                                onClick={() => setActiveIndex(1)}
                                                style={{margin: 20}}
                                            >
                                                <Image src={color.source} style={{margin: 10}}/>
                                                <Card.Content style={{height: 35}}>
                                                    <Card.Header>
                                                        <Label as='a' tag color={color.color}>
                                                            {color.name}
                                                        </Label>
                                                    </Card.Header>
                                                </Card.Content>
                                            </Card>
                                        );
                                    })}
                                </div>
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
                    <ChatComponent />
                </NetworkManager>
            }
        </>
    );
}

export default App;
