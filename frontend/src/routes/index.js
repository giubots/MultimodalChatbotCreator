import React from 'react';
import {Switch, Route, Link} from 'react-router-dom';
import SimpleChatApp from '../pages/SimpleChatApp';
import {StoreApp} from '../pages/StoreApp';
import {Divider, Icon} from "semantic-ui-react";

const ChoosePage = () => {
    return (
        <div style={styles.container}>
            <h3>Choose route</h3>
            <Link class="ui button teal" to={"/simple-chat"}>
                <Icon name={"chat"}/>
                Simple chat App
            </Link>
            <Divider/>
            <Link class="ui button purple" to={"/store"}>
                <Icon name={"shop"}/>
                Store App
            </Link>
        </div>
    )
}

export default function Routes() {
    return (
        <Switch>
            <Route path="/" exact component={ChoosePage}/>
            <Route path="/simple-chat" component={SimpleChatApp}/>
            <Route path="/store" component={StoreApp}/>
        </Switch>
    );
}

const styles = {
    container: {
        height: "100vh",
        display: "flex",
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column"
    }
}
