import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { Context, Provider } from "./components/globalContext/globalContext.js";
import { View } from "react-native";
import Navigator from "./components/navigation/navigator.js";

function App() {
    return (
        // it passes the global context variables through the different layers
        <Provider>
        <View style={{ flex: 1 }}>
            <NavigationContainer>
                <Navigator />
            </NavigationContainer>
        </View>
        </Provider>
    )
}

export default App;