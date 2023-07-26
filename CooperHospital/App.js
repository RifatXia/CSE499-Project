// import React, { useState, useEffect } from 'react';
// import { Button, StyleSheet, Text, View, SafeAreaView } from 'react-native';

// const url = "https://reactnative.dev/movies.json";

// const App = () => {

//     return (
//         <SafeAreaView style={ styles.body }>
//             <Text style={ styles.text }>Hello Zia</Text>
//         </SafeAreaView>
//     );
// };

// export default App;

import { Text, View, Image } from 'react-native'
import React, { Component } from 'react'
import { GoogleSignin, GoogleSigninButton } from '@react-native-community/google-signin'

// get the google client ID from Google OAuth 
GoogleSignin.configure({
    webClientId: '248229658628-cd6s6cauehhb8qs9a8m2uk1t88rmhkn5.apps.googleusercontent.com',
    offlineAccess: true
})

export class App extends Component {
    constructor(props){
        super(props);
        this.state = {
            userGoogleInfo: {},
            loaded: false
        };
    }

    // signin function to fetch the user info 
    signIn = async() => {
        try{
            await GoogleSignin.hasPlayServices()
            const userInfo = await GoogleSignin.signIn();
            this.state({
                userGoogleInfo: userInfo,
                loaded: true
            })
        }
        catch(error){
            console.log(error.message);
        }
    }
    
    render() {
        return (
            <View>
                <GoogleSigninButton
                    onPress={ this.signIn }
                    size={ GoogleSigninButton.Size.Wide }
                    color={ GoogleSigninButton.Color.Dark }
                    style={ styles.sign_in }
                />
                {
                    this.state.loaded ? (
                        <View>
                            <Text>this.state.userGoogleInfo.user.name</Text>
                            <Text>this.state.userGoogleInfo.user.email</Text>
                            <Image style={ styles.sign_in } source={{ uri:this.state.userGoogleInfo.user.photo }} ></Image>
                        </View>
                    ) : (
                        <Text>Not Signed In</Text>
                    )
                }
            </View>
        )
    }
}

const styles = StyleSheet.create({
    body:{
        backgroundColor: '#000000',
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    // color and text of the font
    text:{
        color:'#ffffff',
        fontSize: 20,
        fontFamily: 'Italic',
    },
    sign_in:{
        width:100,
        height:100,
    },
});

export default App