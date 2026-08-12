# Embedded Controller Cross-Format Example

- Model ID: `example.embedded-controller`
- Type: `electronics-system`

## Elements

### MCU

- ID: `mcu`
- Type: `component`

| Property | Value |
|---|---|
| role | controller |

### Temperature Sensor

- ID: `sensor`
- Type: `component`

| Property | Value |
|---|---|
| interface | I2C |

### Radio

- ID: `radio`
- Type: `component`

| Property | Value |
|---|---|
| interface | SPI |

## Relationships

| ID | Type | Source | Target | Direction | Label |
|---|---|---|---|---|---|
| r1 | communication | mcu | sensor | bidirectional | I2C |
| r2 | communication | mcu | radio | bidirectional | SPI |
