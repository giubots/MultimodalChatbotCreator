import React, {useState} from "react";
import {Components, NetworkManager} from "../react-chatbot-ui";
import 'semantic-ui-css/semantic.min.css'
import {Accordion, Icon, Card, Image, Button, Label, Form} from 'semantic-ui-react'
import {ChatComponent} from "../components/ChatComponent";
import {data} from "../Constants";

export function StoreApp() {

    const [messages, setMessages] = useState([]);
    const uid = sessionStorage.getItem("uid");
    const [activeIndex, setActiveIndex] = useState(0);
    const [size, setSize] = useState(0);

    const [choice, setChoice] = useState();
    const [colorChoice, setColorChoice] = useState();

    const [delivery, setDelivery] = useState();
    const [payment, setPayment] = useState();


    const handleClick = (e, titleProps) => {
        const {index} = titleProps
        const newIndex = activeIndex === index ? -1 : index
        setActiveIndex(newIndex);
    }


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
                    onMessage={(m) => setMessages([...messages, {from: "Chat", message: JSON.parse(m).utterance}])}
                    onOpen={() => setMessages([...messages, {from: "Socket", message: "Connection opened!"}])}
                    onClose={() => setMessages([...messages, {from: "Socket", message: "Connection closed!"}])}
                    onError={() => setMessages([...messages, {from: "Socket", message: "Error in connection!"}])}
                >
                    <div style={{...styles.container, marginTop: 30}}>
                        <Accordion style={{width: 1000}} styled>

                            {/** Item to buy **/}

                            <Accordion.Title
                                active={activeIndex === 0}
                                index={0}
                                onClick={handleClick}
                            >
                                <Icon name='dropdown'/>
                                Choose the item to buy:
                            </Accordion.Title>
                            <Accordion.Content active={activeIndex === 0}>
                                <div style={styles.container}>
                                    {data.map((item, index) => {
                                        return (
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
                                        );
                                    })}
                                </div>
                            </Accordion.Content>

                            {/** Size **/}

                            <Accordion.Title
                                active={activeIndex === 1}
                                index={1}
                                onClick={handleClick}
                            >
                                <Icon name='dropdown'/>
                                Choose size
                            </Accordion.Title>
                            <Accordion.Content active={activeIndex === 1}>
                                <div style={styles.container}>
                                    <Button.Group>
                                        {data[choice]?.sizes.map((s, i) => {
                                            return (
                                                <>
                                                    {i !== 0 && (<Button.Or/>)}
                                                    <Components.OnClick>
                                                        <Button
                                                            color={size === s.key && 'teal'}
                                                            onClick={() => setSize(s.key)}
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

                            <Accordion.Title
                                active={activeIndex === 2}
                                index={2}
                                onClick={handleClick}
                            >
                                <Icon name='dropdown'/>
                                Choose color
                            </Accordion.Title>
                            <Accordion.Content active={activeIndex === 2}>
                                <div style={styles.container}>
                                    {data[choice]?.colors.map((color, index) => {
                                        return (
                                            <Card
                                                onClick={() => setColorChoice(index)}
                                                raised={colorChoice === index}
                                                style={{margin: 20}}
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
                                        );
                                    })}
                                </div>
                            </Accordion.Content>

                            <Accordion.Title
                                active={activeIndex === 3}
                                index={3}
                                onClick={handleClick}
                            >
                                <Icon name='dropdown'/>
                                Payment method
                            </Accordion.Title>
                            <Accordion.Content active={activeIndex === 3}>
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

                            <Accordion.Title
                                active={activeIndex === 4}
                                index={4}
                                onClick={handleClick}
                            >
                                <Icon name='dropdown'/>
                                Address
                            </Accordion.Title>
                            <Accordion.Content active={activeIndex === 4}>
                                <Components.OnSubmit>
                                    <Form>
                                        <Form.Group unstackable widths={2}>
                                            <Form.Input label='First name' placeholder='First name'/>
                                            <Form.Input label='Last name' placeholder='Last name'/>
                                        </Form.Group>
                                        <Form.Group widths={2}>
                                            <Form.Input label='Address' placeholder='Address'/>
                                            <Form.Input label='Phone' placeholder='Phone'/>
                                        </Form.Group>
                                        <Form.Checkbox label='I agree to the Terms and Conditions'/>
                                        <Button type='submit'>Confirm</Button>
                                    </Form>
                                </Components.OnSubmit>
                            </Accordion.Content>

                            <Accordion.Title
                                active={activeIndex === 5}
                                index={5}
                                onClick={handleClick}
                            >
                                <Icon name='dropdown'/>
                                Delivery method
                            </Accordion.Title>
                            <Accordion.Content active={activeIndex === 5}>
                                <Components.OnSubmit payload={{delivery}}>
                                    <Form>
                                        <Form.Group>
                                            <Form.Radio
                                                label='Standard delivery (FREE)'
                                                value='standard'
                                                checked={delivery === 'standard'}
                                                onChange={() => setDelivery("standard")}
                                            />
                                            <Form.Radio
                                                label='Express delivery (14.33$)'
                                                value='express'
                                                checked={delivery === 'express'}
                                                onChange={() => setDelivery("express")}
                                            />
                                            <Button type='submit'>Place order</Button>
                                        </Form.Group>
                                    </Form>
                                </Components.OnSubmit>
                            </Accordion.Content>
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
        flex: 1,
        flexDirection: "flex-row",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
    },
}
