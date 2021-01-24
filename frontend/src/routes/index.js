import React from 'react';
import {Switch, Route, Link} from 'react-router-dom';
import SimpleChatApp from '../pages/SimpleChatApp';
import {StoreApp} from '../pages/StoreApp';

const ChoosePage = () => {
    return (
        <div style={{display: "flex", flex: 1, justifyContent: "center", alignItems: "center", flexDirection: "column"}}>
            <Link class="ui button" to={"/simple-chat"} >Simple chat App</Link>
            <Link class="ui button" to={"/store"} >Store App</Link>
        </div>
    )
}



export default function Routes() {
    return (
        <Switch>
            <Route path="/" exact component={ChoosePage} />
            <Route path="/simple-chat" component={SimpleChatApp} />
            <Route path="/store" component={StoreApp} />
        </Switch>
    );
}
