import React from 'react';
import {AbsoluteFill, Composition, registerRoot} from 'remotion';

const Teste = () => <AbsoluteFill style={{backgroundColor: '#10283f', color: 'white', justifyContent: 'center', alignItems: 'center', fontFamily: 'Arial', fontSize: 48}}>Ambiente de edição ESNAUTO</AbsoluteFill>;
const Root = () => <Composition id="Teste" component={Teste} durationInFrames={30} fps={30} width={1280} height={720}/>;
registerRoot(Root);
