import React from "react";
import { createStackNavigator } from "@react-navigation/stack"
import { View } from "react-native";
import Landing from "../screens/landing.js";

const Stack = createStackNavigator();

function Navigator(props){
    // setting the landing page 
    <Stack.Navigator initialRouteName="Landing">
        <Stack.Screen name = "Landing" component={Landing} options={{ headerShown: false }}/>
    </Stack.Navigator>
}
export default Navigator;