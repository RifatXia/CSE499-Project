import React, { useContext } from 'react';
import { View, Text } from 'react-native';
import { Context } from "../globalContext/globalContext.js"
import { styles } from '../globalContext/style.js';

function Landing(props){

  const globalContext = useContext(Context)
  const { isLoggedIn } = globalContext;

  return(
    <View>
      <Text style={ styles.text }>Hello User!</Text>
      <Text style={ styles.text }>You are {(isLoggedIn)? '' : "Not "}logged in</Text>
    </View>
  )

}

export default Landing;
