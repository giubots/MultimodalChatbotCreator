import React, {useState} from "react";
import {Components, NetworkManager} from "../react-chatbot-ui";
import 'semantic-ui-css/semantic.min.css'
import {Accordion, Icon, Card, Image, Button, Label, Form} from 'semantic-ui-react'
import {ChatComponent} from "../components/ChatComponent";
import {data} from "../Constants";


export function StoreApp() {

    const [messages, setMessages] = useState([]);
    const [payload, setPayload] = useState({});

    const uid = sessionStorage.getItem("uid");
    const [activeIndex, setActiveIndex] = useState(0);
    const [activeIndexSub, setActiveIndexSub] = useState(-1);

    const [size, setSize] = useState(0);

    const [choice, setChoice] = useState();
    const [colorChoice, setColorChoice] = useState();

    const [payment, setPayment] = useState();


    const handleClick = (e, titleProps, key) => {
        if (payload[key]) {
            const {index} = titleProps
            const newIndex = activeIndex === index ? -1 : index
            setActiveIndex(newIndex);
            setActiveIndexSub(-1);
        }
    }

    const process = [
        {
            key: "show_items",
            title: "Choose the item to buy",
            content: () => {
                return (
                    <div style={styles.container}>
                            {data.map((item, index) => {
                                return (
                                    <div key={index}>
                                        <Components.OnClick
                                            payload={{intent: "state_preference", preference: item.key}}
                                        >
                                            <Card
                                                raised={choice === index}
                                                onClick={() => {
                                                    if (item.availability) {
                                                        setActiveIndex(1);
                                                        setChoice(index);
                                                    }
                                                }}
                                                style={{margin: 20}}
                                            >
                                                <Image src={item.source} disabled={!item.availability}
                                                       style={{margin: 10}}/>
                                                <Card.Content style={{height: 70}}>
                                                    <Card.Header>{item.name}</Card.Header>
                                                </Card.Content>
                                                <Card.Content extra>
                                                    <Icon name={item.availability ? 'check' : "remove"}/>
                                                    {item.availability || "No"} pairs available
                                                </Card.Content>
                                            </Card>
                                        </Components.OnClick>
                                    </div>
                                );
                            })}
                        </div>
                );
            },
        },
        {
            key: "choose_customize",
            title: "Customization",
            content: () => {
                return (
                    <div style={styles.innerContainer}>
                            <Accordion style={{flex: 1, width: "100%"}}>

                                {/** Size **/}

                                <Accordion.Title
                                    active={activeIndexSub === 0}
                                    index={0}
                                    onClick={() => setActiveIndexSub(0)}
                                >
                                    <Components.OnClick
                                        payload={{intent: "change_something", change: "size"}}
                                    >
                                        <Icon name='dropdown'/>
                                        Choose size
                                    </Components.OnClick>
                                </Accordion.Title>
                                <Accordion.Content active={activeIndexSub === 0}>
                                    <div style={styles.container}>
                                        <Button.Group>
                                            {data[choice]?.sizes.map((s, index) => {
                                                return (
                                                    <>
                                                        {index !== 0 && (<Button.Or/>)}
                                                        <Components.OnClick
                                                            payload={{
                                                                intent: "state_preference",
                                                                preference: s.key
                                                            }}
                                                        >
                                                            <Button
                                                                color={size === s.key && 'teal'}
                                                                onClick={() => {
                                                                    setSize(s.key);
                                                                    setActiveIndexSub(-1);
                                                                }}
                                                                active={size === s.key}
                                                            >{s.name}
                                                            </Button>
                                                        </Components.OnClick>
                                                    </>
                                                )
                                            })}
                                        </Button.Group>
                                    </div>
                                </Accordion.Content>

                                {/** Color **/}

                                <Components.OnClick
                                    payload={{intent: "change_something", change: "color"}}
                                >
                                    <Accordion.Title
                                        active={activeIndexSub === 1}
                                        index={1}
                                        onClick={() => setActiveIndexSub(1)}
                                    >
                                        <Icon name='dropdown'/>
                                        Choose color
                                    </Accordion.Title>
                                </Components.OnClick>
                                <Accordion.Content active={activeIndexSub === 1}>
                                    <div style={styles.container}>
                                        {data[choice]?.colors.map((color, index) => {
                                            return (
                                                <Components.OnClick
                                                    key={index}
                                                    payload={{
                                                        intent: "state_preference",
                                                        preference: color.key
                                                    }}
                                                >
                                                    <Card
                                                        style={{margin: 20}}
                                                        onClick={() => {
                                                            setColorChoice(index);
                                                            setActiveIndexSub(-1);
                                                        }}
                                                        raised={colorChoice === index}
                                                    >
                                                        <Image src={color.source} style={{margin: 10}}/>
                                                        <Card.Content style={{height: 35}}>
                                                            <Card.Header>
                                                                <Label as='a' tag color={color.key}>
                                                                    {color.name}
                                                                </Label>
                                                            </Card.Header>
                                                        </Card.Content>
                                                    </Card>
                                                </Components.OnClick>
                                            );
                                        })}
                                    </div>
                                </Accordion.Content>
                            </Accordion>
                            <Components.OnClick
                                disabled={!payload["custom_completed"]}
                                payload={{intent: "change_nothing"}}
                            >
                                <Button
                                    disabled={!payload["custom_completed"]}
                                    style={styles.button}
                                    onClick={() => setActiveIndex(2)}
                                >
                                    <Icon name={"angle double down"}/>
                                    Continue
                                </Button>
                            </Components.OnClick>
                        </div>
                );
            }
        },
        {
            key: "choose_info",
            title: "Details",
            content: () => {
                return (
                    <div style={styles.innerContainer}>
                        <Accordion style={{flex: 1, width: "100%"}}>

                            <Accordion.Title
                                active={activeIndexSub === 0}
                                index={0}
                                onClick={() => setActiveIndexSub(0)}
                            ><Components.OnClick
                                payload={{intent: "change_something", change: "payment"}}>
                                <Icon name='dropdown'/>
                                Payment method
                            </Components.OnClick>
                            </Accordion.Title>
                            <Accordion.Content active={activeIndexSub === 0}>
                                <Components.OnSubmit payload={{payment}}>
                                    <Form>
                                        <Form.Group>
                                            <Form.Radio
                                                label='Credit card (ending with -5698)'
                                                value='credit_card'
                                                checked={payment === 'credit_card'}
                                                onChange={() => setPayment("credit_card")}
                                            />
                                            <Form.Radio
                                                label='PayPal account (gino@outlook.com)'
                                                value='paypal'
                                                checked={payment === 'paypal'}
                                                onChange={() => setPayment("paypal")}
                                            />
                                            <Button type='submit'>Confirm</Button>
                                        </Form.Group>
                                    </Form>
                                </Components.OnSubmit>
                            </Accordion.Content>
                            <Components.OnClick
                                payload={{intent: "change_something", change: "address"}}
                            >
                                <Accordion.Title
                                    active={activeIndexSub === 1}
                                    index={1}
                                    onClick={() => setActiveIndexSub(1)}
                                >
                                    <Icon name='dropdown'/>
                                    Address
                                </Accordion.Title>
                            </Components.OnClick>

                            <Accordion.Content active={activeIndexSub === 1}>
                                <Components.OnSubmit
                                    payload={{}}
                                >
                                    <Form>
                                        <Form.Group widths={2}>
                                            <Form.Field>
                                                <label>First Name</label>
                                                <input placeholder={'First Name'} type={'text'}/>
                                            </Form.Field>
                                            <Form.Field>
                                                <label>Last Name</label>
                                                <input placeholder={'Last Name'} type={'text'}/>
                                            </Form.Field>
                                        </Form.Group>
                                        <Form.Group widths={2}>
                                            <Form.Field>
                                                <label>Address</label>
                                                <input placeholder={'Address'} type={'text'}/>
                                            </Form.Field>
                                            <Form.Field>
                                                <label>Phone</label>
                                                <input placeholder={'Phone'} type={'text'}/>
                                            </Form.Field>
                                        </Form.Group>
                                        <Form.Checkbox label='I agree to the Terms and Conditions'/>
                                        <Button type='submit'>Confirm</Button>
                                    </Form>
                                </Components.OnSubmit>
                            </Accordion.Content>
                        </Accordion>
                        <Components.OnClick
                            payload={{intent: "change_nothing"}}
                        >
                            <Button style={styles.button}>
                                <Icon name={"angle double down"}/>
                                Continue
                            </Button>
                        </Components.OnClick>
                    </div>
                );
            }
        },
        {
            key: "complete",
            title: "Summary",
            content: () => {
                return (
                    <Button>Complete purchase</Button>
                );
            }
        },
    ];

    return (
        <>
            {!uid ?
                <div className={"login-container"}>
                    <label>Insert username and press enter</label>
                    <br/>
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
                    onMessage={(m) => {
                        setMessages([...messages, {from: "Chat", message: JSON.parse(m).utterance}]);
                        setPayload(JSON.parse(m).payload);
                    }}
                    onOpen={() => setMessages([...messages, {from: "Socket", message: "Connection opened!"}])}
                    onClose={() => setMessages([...messages, {from: "Socket", message: "Connection closed!"}])}
                    onError={() => setMessages([...messages, {from: "Socket", message: "Error in connection!"}])}
                >
                    <div style={{...styles.container, marginTop: 30}}>
                        <Accordion style={{width: 1000}} styled>
                            {process.map((e, i) => {
                                return (
                                    <>
                                        <Accordion.Title
                                            active={activeIndex === i}
                                            index={i}
                                            onClick={(ev, p) => handleClick(ev, p, e.key)}
                                        >
                                            <Icon name='dropdown'/>
                                            {e.title}
                                        </Accordion.Title>
                                        <Accordion.Content active={activeIndex === i}>
                                            {e.content()}
                                        </Accordion.Content>
                                    </>
                                );
                            })}
                        </Accordion>

                    </div>
                    <ChatComponent messagesProps={messages} setMessagesProps={(messages => setMessages(messages))}/>
                </NetworkManager>
            }
        </>
    );
}

const styles = {
    container: {
        width: "100%",
        flex: 1,
        flexDirection: "row",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
    },
    innerContainer: {
        width: "100%",
        flex: 1,
        flexDirection: "column",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
    },
    button: {
        marginTop: 20,
        width:"100%",
    },
}
