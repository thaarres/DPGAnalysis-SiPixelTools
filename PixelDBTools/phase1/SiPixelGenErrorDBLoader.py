import FWCore.ParameterSet.Config as cms
import sys
process = cms.Process("SiPixelGenErrorDBUpload")

process.load("CondCore.DBCommon.CondDBCommon_cfi")
process.load("FWCore.MessageService.MessageLogger_cfi")
#process.load("Configuration.Geometry.GeometryDB_cff")
process.load("Configuration.Geometry.GeometryExtended2017Reco_cff")

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
# from Configuration.AlCa.GlobalTag import GlobalTag
# works with condDB and condDBv2
# process.GlobalTag = GlobalTag(process.GlobalTag, '74X_dataRun2_Prompt_v3', '')
# process.GlobalTag = GlobalTag(process.GlobalTag, 'GR_R_75_V1A', '')
# process.GlobalTag = GlobalTag(process.GlobalTag, 'FT_R_74_V15B', '')
# process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')
# process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_design', '')
# process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2017_design', '')
process.GlobalTag = GlobalTag(process.GlobalTag, '75X_upgrade2017_design_v4', '')

MagFieldValue = 3.8
#MagFieldString = '38T'
files_to_upload = cms.vstring(
        "../../DB/MC/generror_summary_zp0030.out",
        "../../DB/MC/generror_summary_zp0031.out"
)
theDetIds      = cms.vuint32( 1, 2)
theGenErrorIds = cms.vuint32(30,31)
generror_base = "SiPixelGenErrorDBObject_phase1_38T_MC_v1"

process.source = cms.Source("EmptyIOVSource",
                            timetype = cms.string('runnumber'),
                            firstValue = cms.uint64(1),
                            lastValue = cms.uint64(1),
                            interval = cms.uint64(1)
                            )

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
    )

process.PoolDBOutputService = cms.Service("PoolDBOutputService",
    DBParameters = cms.PSet(
     messageLevel = cms.untracked.int32(0),
     authenticationPath = cms.untracked.string('.')
    ),
    timetype = cms.untracked.string('runnumber'),
    connect = cms.string('sqlite_file:SiPixelGenErrorDBObject_phase1_38T_mc_v1.db'),
    toPut = cms.VPSet(cms.PSet(
     record = cms.string('SiPixelGenErrorDBObjectRcd'),
     tag = cms.string("SiPixelGenErrorDBObject_phase1_38T_mc_v1")
    ))
)

process.uploader = cms.EDAnalyzer("SiPixelGenErrorDBObjectUploader",
                                  siPixelGenErrorCalibrations = files_to_upload,
                                  theGenErrorBaseString = cms.string(generror_base), # ???
                                  Version = cms.double("1.0"),  # ???
                                  MagField = cms.double(3.8),  # why needed?
                                  detIds = theDetIds,
                                  generrorIds = theGenErrorIds
)


process.p = cms.Path(process.uploader)
