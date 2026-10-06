# Soapmaker

A Project Zomboid Build 42 mod: make your own soap, and the lard it needs.

- **Mix Soap** (must be learned): 1 full Lard + 1 Charcoal + 1 L of water from a cooking pot (kept) gives 2 Raw Soap. Crafted from the inventory, no table or fire needed.
- **Raw Soap** cooks like food: 60 in-game minutes in an oven, on a campfire, barbecue or fireplace turns each into a full soap bar. It can't be eaten.
- **Learning it**: read *"Fight Club" by Chuck Palahniuk* or the magazine *Soapmaker's Guide to Galaxy*. The book spawns wherever vanilla fiction books do and the magazine wherever *Good Cooking* does, with the same odds.
- **Trim Fat** (known by default): 2 raw cuts of Pork, Pork Chop, Beef, Steak, Venison or Mutton Chop plus a knife give 1 Raw Fat, which cooks into Lard in 60 minutes.

Lua and script files only, no Java. Both the server and every player need the mod. English and Polish.

Want to clean with the soap? See [Soapy Water](https://github.com/m-gie/soapywater). The two mods don't depend on each other.

## Development

```
pip install lupa
python tests/run.py
```

`bash workshop.sh` stages the Workshop upload folder in `~/Zomboid/Workshop/Soapmaker`.
