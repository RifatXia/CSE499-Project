import React, { useState, useEffect } from 'react';
import { Button, StyleSheet, Text, View, SafeAreaView } from 'react-native';

const url = "https://reactnative.dev/movies.json";

const App = () => {

    return (
        <SafeAreaView style={ styles.body }>
            <Text style={ styles.text }>Hello Zia</Text>
        </SafeAreaView>
    );
};

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