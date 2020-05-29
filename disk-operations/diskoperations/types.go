package diskoperations

import "errors"

var (
	ErrBackingFileNotFound = errors.New("backing file not found")
	ErrFileNotFound        = errors.New("backing file not found")
)

type ImageInfoQcow2 struct {
	VirtualSize         int64                   `json:virtual-size`
	Filename            string                  `json:filename`
	ClusterSize         int32                   `json:cluster-size`
	Format              string                  `json:format`
	ActualSize          int64                   `json:actual-size`
	FormatSpecific      *ImageInfoSpecificQcow2 `json:format-specific`
	FullBackingFilename string                  `full-backing-filename,omitempty`
	BackingFilename     string                  `backing-filename,omitempty`
	DirtyFlag           bool                    `json:dirty-flag`
	Snapshots           *[]ImageInfoSnapshot    `json:snapshots`
}

type ImageInfoSpecificQcow2 struct {
	Type string                        `json:type`
	Data *ImageInfoSpecificQcow2Detail `json:data`
}

type ImageInfoSpecificQcow2Detail struct {
	Compat        string `json:compat`
	LazyRefcounts bool   `json:lazy-refcounts`
	RefcountBits  int32  `json:refcount-bits`
	Corrupt       bool   `json:corrupt`
}

type ImageInfoSnapshot struct {
	VmClockNsec int    `json:vm-clock-nsec`
	Name        string `json:name`
	DateSec     int64  `json:date-sec`
	DateNsec    int64  `json:date-nsec`
	Id          string `json:id`
	VmStateSize int64  `json:vm-state-size`
}

/* [
    {
        "snapshots": [
            {
                "vm-clock-nsec": 0,
                "name": "prova",
                "date-sec": 1590675867,
                "date-nsec": 87443000,
                "vm-clock-sec": 0,
                "id": "1",
                "vm-state-size": 0
            }
        ],
        "virtual-size": 1073741824,
        "filename": "test.qcow2",
        "cluster-size": 65536,
        "format": "qcow2",
        "actual-size": 208896,
        "format-specific": {
            "type": "qcow2",
            "data": {
                "compat": "1.1",
                "lazy-refcounts": false,
                "refcount-bits": 16,
                "corrupt": false
            }
        },
        "dirty-flag": false
    }
] */
