import React, {useState} from "react";
import {Components, NetworkManager} from "../react-mmcc";
import 'semantic-ui-css/semantic.min.css'
import {Accordion, Icon, Card, Image, Button, Label, Form, Table} from 'semantic-ui-react'
import {ChatComponent} from "../components/ChatComponent";
import {data} from "../Constants";


export function StoreApp() {

    const [messages, setMessages] = useState([]);
    const [payload, setPayload] = useState({});
    const uid = sessionStorage.getItem("uid");

    const [size, setSize] = useState(0);

    const [choice, setChoice] = useState();
    const [colorChoice, setColorChoice] = useState();

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
                                    <Components.OnClick payload={{intent: "state_preference", preference: item.key}}>
                                        <Card
                                            raised={choice === index}
                                            onClick={() => {
                                                if (item.availability) {
                                                    setChoice(index);
                                                }
                                            }}
                                            style={{margin: 20,}}
                                        >
                                            <Image
                                                src={item.source} disabled={!item.availability}
                                                style={{
                                                    margin: 10,
                                                    cursor: !item.availability && "not-allowed",
                                                }}
                                            />
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
                                active={payload["show_size"]}
                                index={0}
                            >
                                <Components.OnClick
                                    payload={{intent: "change_something", change: "size"}}
                                >
                                    <Icon name='dropdown'/>
                                    Choose size
                                </Components.OnClick>
                            </Accordion.Title>
                            <Accordion.Content active={payload["show_size"]}>
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

                            <Components.OnClick
                                payload={{intent: "change_something", change: "color"}}
                            >
                                <Accordion.Title
                                    active={payload["show_color"]}
                                    index={1}
                                >
                                    <Icon name='dropdown'/>
                                    Choose color
                                </Accordion.Title>
                            </Components.OnClick>
                            <Accordion.Content active={payload["show_color"]}>
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
                                                    onClick={() => setColorChoice(index)}
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

                            {/** Address **/}

                            <Accordion.Title
                                active={payload["show_address"]}
                                index={1}
                            >
                                <Components.OnClick
                                    payload={{intent: "change_something", change: "address"}}
                                >
                                    <Icon name='dropdown'/>
                                    Address
                                </Components.OnClick>
                            </Accordion.Title>
                            <Accordion.Content active={payload["show_address"]}>
                                <div style={styles.container}>
                                    <Components.OnSubmit
                                        intent={"give_address"}
                                        keyType={"label"}
                                    >
                                        <Form style={{
                                            flexDirection: "column",
                                            flex: 1,
                                            display: "flex",
                                            alignItems: "center"
                                        }}>
                                            <Form.Field>
                                                <label>address</label>
                                                <input style={{width: 700}} placeholder={'Type your address here'}
                                                       type={'text'}/>
                                            </Form.Field>
                                            <Button style={{width: 200}} size={"normal"} type='submit'>Confirm</Button>
                                        </Form>
                                    </Components.OnSubmit>
                                </div>

                            </Accordion.Content>

                            {/** Payment **/}

                            <Accordion.Title
                                active={payload["show_payment"]}
                                index={0}
                            >
                                <Components.OnClick
                                    payload={{intent: "change_something", change: "payment"}}>
                                    <Icon name='dropdown'/>
                                    Payment method
                                </Components.OnClick>
                            </Accordion.Title>
                            <Accordion.Content active={payload["show_payment"]}>
                                <Components.OnSubmit
                                    keyType={"attribute"}
                                    attributeName={"name"}
                                    intent={"payment_details"}
                                    blacklist={["submit"]}
                                >
                                    <Form style={{marginBottom: 40, marginTop: 20}}>
                                        <Form.Group style={{
                                            flexDirection: "row",
                                            flex: 1,
                                            display: "flex",
                                            alignItems: "center"
                                        }}>
                                            <Form.Input
                                                style={{width: 700}}
                                                placeholder='Credit card number'
                                                name={"details"}
                                                icon={"credit card"}
                                            />
                                            <Form.Button content='Submit' size={"big"}/>
                                        </Form.Group>
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
                let purchase = payload["useful_variables"];
                let item = data.find(e => e.key === purchase?.item);
                let color = item?.colors.find(c => c.key === purchase?.color)

                return (
                    <>
                        {item && (
                            <div style={styles.container}>
                                <Table definition style={{margin: 10}}>
                                    <Table.Header>
                                        <Table.Row>
                                            <Table.HeaderCell />
                                            <Table.HeaderCell>Your purchase details</Table.HeaderCell>
                                        </Table.Row>
                                    </Table.Header>

                                    <Table.Body>
                                        <Table.Row>
                                            <Table.Cell>Item name</Table.Cell>
                                            <Table.Cell>{item.name}</Table.Cell>
                                        </Table.Row>
                                        <Table.Row>
                                            <Table.Cell>Size</Table.Cell>
                                            <Table.Cell>{purchase.size}</Table.Cell>
                                        </Table.Row>
                                        <Table.Row>
                                            <Table.Cell>Color</Table.Cell>
                                            <Table.Cell>{color.name}</Table.Cell>
                                        </Table.Row>
                                        <Table.Row>
                                            <Table.Cell>Delivery address</Table.Cell>
                                            <Table.Cell>{purchase.address}</Table.Cell>
                                        </Table.Row>
                                        <Table.Row>
                                            <Table.Cell>Payment details</Table.Cell>
                                            <Table.Cell>{purchase.payment}</Table.Cell>
                                        </Table.Row>
                                    </Table.Body>
                                </Table>
                                <Card style={{margin: 10}}>
                                    <Image src={color.source} style={{margin: 10}}/>
                                    <Card.Content style={{height: 35}}>
                                        <Card.Header>
                                            <Label as='a' tag color={color.key}>
                                                {color.name}
                                            </Label>
                                        </Card.Header>
                                    </Card.Content>
                                </Card>
                            </div>
                        )}
                    </>
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
                        <Accordion style={{width: 1200}} styled>
                            {process.map((e, i) => {
                                let active = payload[e.key];
                                return (
                                    <>
                                        <Accordion.Title
                                            style={{
                                                backgroundColor: !active && "whitesmoke",
                                                cursor: !active && "not-allowed",
                                            }}
                                            active={active}
                                            index={i}
                                        >
                                            <Icon name='dropdown'/>
                                            {e.title}
                                        </Accordion.Title>
                                        <Accordion.Content active={active}>
                                            {e.content()}
                                        </Accordion.Content>
                                    </>
                                );
                            })}
                        </Accordion>

                    </div>
                    {/*<div>
                        PAYLOAD:
                        {Object.keys(payload).map(k => {
                            return (
                                <div style={{flexDirection: "row", display: "flex"}}>
                                    <p>{k}:</p>
                                    <p>{JSON.stringify(payload[k])}</p>
                                </div>
                            );
                        })}
                    </div>*/}
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
        width: "100%",
    },
}
