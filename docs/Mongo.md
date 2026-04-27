# UDM Pro MongoDB Access and Management

## Connection

### SSH Access
```bash
ssh root@<udm-ip>
```

### MongoDB Connection
```bash
mongo --port 27117
```

MongoDB runs on port 27117 (not default 27017).

### Select Database
```javascript
use ace
```

The UniFi database is named `ace`.

## Querying Data

### View Firewall Groups
```javascript
// All firewall groups
db.firewallgroup.find().pretty()

// IP address groups only
db.firewallgroup.find({"group_type": "address-group"}).pretty()

// Port groups only
db.firewallgroup.find({"group_type": "port-group"}).pretty()

// IPv6 groups only
db.firewallgroup.find({"group_type": "ipv6-address-group"}).pretty()

// Summary view (names and members only)
db.firewallgroup.find({}, {name: 1, group_type: 1, group_members: 1, _id: 0}).pretty()
```

### View Other Collections
```javascript
// User/Client groups
db.usergroup.find().pretty()

// Network configurations
db.networkconf.find().pretty()

// List all collections
show collections

// List all databases
show dbs
```

### One-liner Queries (from SSH)
```bash
mongo --port 27117 ace --eval "db.firewallgroup.find().pretty()"
```

## Updating Data

### Basic Update Operations

#### Replace Array
```javascript
db.firewallgroup.updateOne(
  { "name": "YourGroupName" },
  { $set: { "group_members": ["192.168.1.10", "192.168.1.20", "192.168.1.30"] } }
)
```

#### Update Multiple Fields
```javascript
db.firewallgroup.updateOne(
  { "name": "YourGroupName" },
  { $set: { 
      "group_members": ["192.168.1.10", "192.168.1.20"],
      "group_members_ipv6": []
    } 
  }
)
```

#### Add Single Item to Array
```javascript
db.firewallgroup.updateOne(
  { "name": "YourGroupName" },
  { $addToSet: { "group_members": "192.168.1.50" } }
)
```

#### Add Multiple Items to Array
```javascript
db.firewallgroup.updateOne(
  { "name": "YourGroupName" },
  { $addToSet: { "group_members": { $each: ["192.168.1.50", "192.168.1.51"] } } }
)
```

#### Remove Item from Array
```javascript
db.firewallgroup.updateOne(
  { "name": "YourGroupName" },
  { $pull: { "group_members": "192.168.1.10" } }
)
```

### MongoDB Update Operators

| Operator | Function |
|----------|----------|
| `$set` | Set field value(s) |
| `$unset` | Remove field |
| `$addToSet` | Add to array (no duplicates) |
| `$push` | Add to array (allows duplicates) |
| `$pull` | Remove from array |
| `$inc` | Increment number |

## Workflow

### Recommended Update Sequence

```javascript
// 1. Backup current document
var backup = db.firewallgroup.findOne({"name": "YourGroupName"})
printjson(backup)

// 2. Verify query matches exactly one document
db.firewallgroup.find({"name": "YourGroupName"})

// 3. Execute update
db.firewallgroup.updateOne(
  { "name": "YourGroupName" },
  { $set: { "group_members": ["192.168.1.10", "192.168.1.20"] } }
)

// 4. Verify update result
// Look for: { "acknowledged": true, "matchedCount": 1, "modifiedCount": 1 }

// 5. Confirm changes
db.firewallgroup.findOne({"name": "YourGroupName"})
```

### Backup Database
```bash
mongodump --port 27117 --db ace --out /root/backup-$(date +%Y%m%d)
```

### Restart UniFi Service
```bash
systemctl restart unifi
```

Restart required for controller to reload database changes.

## Notes

- Enable SSH in Settings → System → Advanced
- Direct database modifications may be overwritten by controller
- Backup before modifications
- Verify query scope before executing updates
- Check update result for matchedCount and modifiedCount

