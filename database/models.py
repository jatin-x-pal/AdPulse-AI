from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column("Campaign_ID", Integer, primary_key=True, index=True)
    name = Column("Campaign_Name", String, index=True)
    platform = Column("Platform", String)
    spend = Column("Spend", Float)
    revenue = Column("Revenue", Float)
    clicks = Column("Clicks", Integer)
    impressions = Column("Impressions", Integer)
    conversions = Column("Conversions", Integer)
    date = Column("Date", Date)

    audiences = relationship("Audience", back_populates="campaign")
    metrics = relationship("Metrics", back_populates="campaign", uselist=False)

class Audience(Base):
    __tablename__ = "audiences"

    id = Column("Audience_ID", Integer, primary_key=True, index=True)
    age_group = Column("Age_Group", String)
    gender = Column("Gender", String)
    device = Column("Device", String)
    location = Column("Location", String)
    campaign_id = Column("Campaign_ID", Integer, ForeignKey("campaigns.Campaign_ID"))

    campaign = relationship("Campaign", back_populates="audiences")

class Metrics(Base):
    __tablename__ = "metrics"

    id = Column("Metric_ID", Integer, primary_key=True, index=True)
    ctr = Column("CTR", Float)
    cpc = Column("CPC", Float)
    cpm = Column("CPM", Float)
    roas = Column("ROAS", Float)
    conversion_rate = Column("Conversion_Rate", Float)
    campaign_id = Column("Campaign_ID", Integer, ForeignKey("campaigns.Campaign_ID"))

    campaign = relationship("Campaign", back_populates="metrics")
