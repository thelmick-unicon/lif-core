export default {
  rules: {
    "scope-empty": [2, "never"],
    "scope-case": [2, "always", "upper-case"],
    "scope-min-length": [2, "always", 4],
    "subject-empty": [2, "never"],
    "subject-min-length": [2, "always", 4],
    "header-max-length": [0, "always", 72],
    "body-leading-blank": [2, "always"],
  },
  parserPreset: {
    parserOpts: {
      headerPattern: /^((LIF-|LIFCORE-)\d+(?:, (LIF-|LIFCORE-)\d+)*|NOJIRA):\s(.*)$/,
      headerCorrespondence: ["scope", "subject"],
    },
  },
};
