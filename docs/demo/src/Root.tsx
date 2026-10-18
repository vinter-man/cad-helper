import React from "react";
import {Composition} from "remotion";
import {Demo} from "./Demo";
import {DURATION, FPS} from "./script";

export const Root: React.FC = () => (
  <Composition id="Demo" component={Demo} durationInFrames={DURATION} fps={FPS} width={1280} height={720} />
);
