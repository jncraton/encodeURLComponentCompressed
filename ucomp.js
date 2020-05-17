let encmap = {"er":",","re":"!","in":"'","on":"G","th":"H","st":"I","en":"J","or":"K","an":"L","se":"M","ea":"N","ar":"O","ou":"P","te":"Q","he":"R","al":"S","%2C":"T","%3F":"U","%27":"V","%29":"W","%22":"X","%21":"Y","%20":"Z","%20a":"j","%20s":"q","%20w":"x","%20c":"z","%20t":"?","%20m":"/","%20p":":","%20o":"@","%20f":"-","%20b":"_","%20be":"~","%20of":"$","%20to":"&","%20in":"(","%20he":")","%28%20":"*","%20the":"+","%20and":";",};

function encode(text) {
  text = text.replace(/(^|[\.\!\?] +|\n)([A-Za-z])/g, (c) => {
    return c == c.toUpperCase()
              ? c.toLowerCase()
              : c.toUpperCase()
  })
  return text
}

console.log(encode("Hello, world! Let's make sure sentence casing works properly."))